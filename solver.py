#!/usr/bin/env python2
# -*- coding: utf-8 -*-



import scipy

from scipy.optimize import *


class Node(object):
    """ A thermal node."""
    def __init__(self, name, tmass, temp=0.0, power=(lambda x: 0.0), description=None, boundary=None):
        #import types

        # Uso name, y no number, ya que este es simplemente un numero para
        # identificarlo, puede ser negativo y no consecutivo
        self._name = name
        self._thermal_mass = tmass
        #self._power = types.MethodType(power, self)
        self._power = power
        self._description = description

        self._conductive_neightbours = {}
        self._radiative_neighbours = {}

        if boundary is None:
            # Vamos a adivinar, sigo la nomenclatura del TAK
            # Si el nombre es negativo entonces es de borde
            self._boundary = True if name < 0 else False

        self.T = temp

    def power(self, time):
        return self._power(time)


    def addConductiveNeightbour(self, node_number, c):
        self._conductive_neightbours[node_number] = c

    def addRadiativeNeightbour(self, node_number, k):
        self._radiative_neighbours[node_number] = k

    def addPowerFunction(self, func):
        """ Aca se asigna la funcion que describe la potencia disipada
        por este nodo en el tiempo. La funcion recibe como parametro el
        timepo de simulacion."""

    def isBoundary(self):
        return self._boundary


class ThermalModel(object):
    """ It holds information about nodes and their interconnection."""
    def __init__(self):
        # node name -> node object
        # Los node name son la identificacion de cada nodo que viene desde afuera
        self._nodes_by_name = {}

        # node number -> node object
        # Los node_number son la identificacion interna. Lo uso como indice en
        # las ecuaciones, matrices, etc. No se ve hacia afuera.
        self._nodes_by_number = {}

        # node object -> node number
        self._numbers_by_name = {}
        self._node_counter = 0

    def addNode(self, node):
        self._nodes_by_name[node._name] = node
        self._nodes_by_number[self._node_counter] = node
        self._numbers_by_name[node._name] = self._node_counter
        self._node_counter += 1

    def addConductance(self, node1, node2, c):
        self._nodes_by_name[node1].addConductiveNeightbour(node2, c)
        self._nodes_by_name[node2].addConductiveNeightbour(node1, c)

    def addAdmittance(self, node1, node2, a):
        self._nodes_by_name[node1].addRadiativeNeightbour(node2, a)
        self._nodes_by_name[node2].addRadiativeNeightbour(node1, a)


class FDMExplicit(object):
    """ Finite Differences Method Explicit."""

    SIGMA = 5.67e-12        # Stefan-Boltzmann constant in w/cm^2xK^4
    

    def __init__(self, model, dt=None):
        self.model = model
        self.dt = dt

        self._nodes_count = self.model._node_counter

        # Matriz con los Cij y Kij sumados y acomodados segundo corresponde
        # Ver doctring de _buildCKMatrix
        self.CK = scipy.zeros((self._nodes_count, self._nodes_count*2), dtype=float)

        # Esta es la matriz posta. Tiene multiplicados los dt/Mi y
        # sumados los 1 en los Ti
        self.F = scipy.zeros((self._nodes_count, self._nodes_count*2), dtype=float)

        # Los dt_M los guardo para que se pueden inspeccionar luego
        self.dt_M = scipy.zeros(self._nodes_count, dtype=float)

        self._buildCKMatrix()
        self._buildFMatrix()


    def _buildCKMatrix(self):
        """
        Arma la matriz de coeficientes C y K:
                                        ...
             - Sum(C1j) - Sum(K1j) +    C12   +   K12    +   C13    +  K13
             +     C21  +   K21    - Sum(C2j) - Sum(K2j) +   C23    +  K23
             +     C31  +   K31    +    C32   +   K32    - Sum(C3j) - Sum(K3j)
                                        ...
            donde:
                Sum es la sumatoria para todo j
                Cij el coeficiente conductivo entre i y j
                Kij el coeficiente radiativo entre i y j
        """

        nod_num = self.model._nodes_by_number
        num_name = self.model._numbers_by_name

        for i, node in nod_num.iteritems():

            if node.isBoundary():
                self.dt_M[i] = 0
                continue

            # Acomodo los componentes K en la columna de al lado de los C
            # quedaria: C*T0 K*T0^4 C*T1 K*T1^4 C*T2 K*T2^4 ...

            # Terminos C. Van en las columnas pares
            for j_name, Cij in node._conductive_neightbours.iteritems():
                j = num_name[j_name]

                self.CK[i, i*2] -= Cij
                self.CK[i, j*2] = Cij

            # Terminos K. Van en las columnas impares
            i_ = (i*2)+1
            for j_name, Aij in node._radiative_neighbours.iteritems():
                j_ = (num_name[j_name]*2)+1

                self.CK[i, i_] -= Aij * self.SIGMA
                self.CK[i, j_] = Aij * self.SIGMA

            self.dt_M[i] = self.dt/node._thermal_mass

    def _buildFMatrix(self):
        # FIXME: ver el termino -[1+(dt/Mi)*Sum(Cij)]. Creo que es [1-(dt/Mi)*Sum(Cij)]
        """
        Arma el sistema de ecuaciones explicitas:
            Ti(n+1) = [1-(dt/Mi)*Sum(Cij)]Ti -[(dt/Mi)*Sum(Kij)]Ti^4 + ...
              ... [(dt/Mi)Cij]*Tj + [(dt/Mi)Kij]*Tj^4  ...

            donde:
                Ti(n+1) es la temperatura del nodo i en el paso n+1
                dt es el paso de tiempo
                Mi la masa termica del nodo i
                Cij el coeficiente conductivo entre i y j
                Kij el coeficiente radiativo entre i y j
                Ti la temperatura del nodo i en el tiempo n
                Tj la temperatura del nodo j en el tiempo n

        Si dt no fue especificado en el constructor, se busca un dt para el cual
        el metodo es estable.
        """

       

        nod_num = self.model._nodes_by_number
        for i, node in nod_num.iteritems():

#            if node.isBoundary():
                # La temperatura n+1 es igual a la del tiempo n
#                self.F[i, i*2] = 1
#                continue

            # Como CK es un numpy.array la * es por elemento.
            # TODO: aca deberia checkear por el 0.45. Ojo que para la columna
            # i*2 el alpha es el coeficiente / 2 (o sobre j?)
            self.F[i] = self.CK[i] * self.dt_M[i]

            # Va el 1 de [1-(dt/Mi)*Sum(Cij)]
            self.F[i, i*2] += 1

    def solve(self, start, end):
        import math

        if end < start:
            raise ValueError("end time should be greater than start time.")

#        if itemps is None:
#            # Aca habria que resolver el modelo en estado estacionario y
#            # averiguar las Tini
#            raise ValueError("Missing itemps.")
#
#        if len(itemps) != self.model._node_counter:
#            raise IndexError("Array itemps must have {} elements.".format(self.model._node_counter))

        # Numero de pasos
        n_max = int((end-start)/self.dt)

        # vector tiempo
        self.t = scipy.linspace(start, end, n_max)

        # Matriz de resultados
        self.T = scipy.zeros((self._nodes_count, n_max), dtype=float)

        nod_num = self.model._nodes_by_number

        # Inicializo la primer columna con las temperaturas iniciales
        for i, node in nod_num.iteritems():
            self.T[i,0] = node.T

        # Vector T pero con las componentes T^4
        # Seria T0(n) T0(n)^4 T1(n) T1(n)^4 T2(n) ...
        T_n = scipy.zeros(self._nodes_count*2, dtype=float)

        for n in range(n_max-1):

            for i, node in nod_num.iteritems():
                # En los indices pares va Ti(n)
                T_n[i*2] = self.T[i,n]

                # En los impares va Ti(n)^4
                T_n[(i*2)+1] = math.pow(self.T[i,n], 4)

            # temp de temporary...
            temp = self.F * T_n

            for i, node in nod_num.iteritems():
                self.T[i,n+1] = reduce(lambda x,y: x+y, temp[i]) + self.dt_M[i]*node.power(self.t[n])
                
# ESTADO ESTACIONARIO

    def solve_stationary(self):
        import math
        nod_num = self.model._nodes_by_number
        P = scipy.zeros(self._nodes_count, dtype=float)

        # Solution
        #T = scipy.zeros(self._nodes_count, dtype=float)

        # The starting estimate for the roots of foo(T)=0
        x0 = scipy.zeros(self._nodes_count, dtype=float) + 300.

        for i, node in nod_num.iteritems():
            P[i] = node.power(0.)
            if node.isBoundary():
                x0[i] = node.T

        def foo(T):
            ret = scipy.zeros(self._nodes_count, dtype=float)
            T_n = scipy.zeros(self._nodes_count*2, dtype=float)

            for i, node in nod_num.iteritems():
                T_n[i*2] = T[i]
                T_n[(i*2)+1] = math.pow(T[i], 4)

            temp = self.CK * T_n

            for i, node in nod_num.iteritems():
                ret[i] = reduce(lambda x, y: x+y, temp[i]) + P[i]

            return ret

            return fsolve(foo, x0)


    def validate_stationary(self, temps):
        import math
        nod_num = self.model._nodes_by_number
        P = scipy.zeros(self._nodes_count, dtype=float)

        # Solution
        T = scipy.zeros(self._nodes_count, dtype=float)

        #x0 = [308.46221541, 327.57380184, 331.01940947, 332.50548799, 327.57380184,
        #          336.80209427, 0.]
        x0 = temps

        for i, node in nod_num.iteritems():
            P[i] = node.power(0.)

        print 'Power: {}'.format(P)

        def foo(T):
            ret = scipy.zeros(self._nodes_count, dtype=float)
            T_n = scipy.zeros(self._nodes_count*2, dtype=float)

            for i, node in nod_num.iteritems():
                T_n[i*2] = T[i]
                T_n[(i*2)+1] = math.pow(T[i], 4)

            temp = self.CK * T_n

            for i, node in nod_num.iteritems():
                ret[i] = reduce(lambda x,y: x+y, temp[i]) + P[i]

            return ret

#        T = newton_krylov(foo, x0)
        T = foo(x0)
 #       print 'Roots: {}'.format(T)
#
        return T

