from copy import copy, deepcopy
import Constraint
import IOHandler


def get_constraints(var, constraints):
    relevant_constraints = []
    constraint: Constraint
    for constraint in constraints:
        if constraint.depends_on(var):
            relevant_constraints.append(constraint)

    return relevant_constraints


def fixed_constraints(solution, constraints):
    fixed_c = []
    constraint: Constraint
    for constraint in constraints:
        if constraint.can_be_evaluated(solution):
            fixed_c.append(constraint)

    return fixed_c


def PCSP(variables, domains, constraints, solution, cost):
    global best_solution
    global best_cost

    if not variables:
        # Dacă nu mai sunt variabile, am ajuns la o soluție mai bună
        print("New best: " + str(cost) + " - " + str(solution))
        # TODO: salvați soluția nou-descoperită
        best_solution = solution
        best_cost = cost
        return True

    elif not domains[variables[0]]:
        # Dacă nu mai sunt valori în domeniu, am terminat căutarea
        return False
    elif cost == best_cost:
        # Dacă am ajuns deja la un cost identic cu cel al celei mai bune soluții, nu mergem mai departe
        return False
    else:
        # TODO: Luăm prima variabilă și prima valoare din domeniu
        var = variables[0]
        val = domains[var].pop(0)

        # TODO: Construim noua soluție
        new_solution = deepcopy(solution)
        new_solution[var] = val

        # TODO: Obținem lista constrângerilor ce pot fi evaluate acum
        valid_constraints = fixed_constraints(new_solution, get_constraints(var, constraints))
        # TODO:  Calculăm costul noii soluții parțiale
        new_cost = cost
        constraint: Constraint
        for constraint in valid_constraints:
            new_cost += constraint.evaluate(new_solution)

        # Verificăm dacă noul cost este mai mic decât cel mai bun cost
        if new_cost < best_cost:
            # Dacă noul cost este mai mic decât cel mai bun cunoscut, rezolvăm pentru restul variabilelor
            # Dacă apelul recursiv întoarce True, a fost găsită o soluție suficient de bună, deci întoarcem True
            if PCSP(variables[1:], deepcopy(domains), constraints, new_solution, new_cost):
                return True

        return PCSP(variables, domains, constraints, solution, cost)


def main():
    global best_solution
    global best_cost

    input = 'input.yml'
    output = 'output.yml'

    io_handler = IOHandler.IOHandler(input)
    [costs, variables, domains, constraints] = io_handler.read_yaml()

    # best_solution = {}
    # best_cost = len(constraints)
    #
    # PCSP(variables, deepcopy(domains), constraints, {}, 0)
    #
    # print("[FINAL] Best found: " + str(best_cost) + " - " + str(best_solution))


if __name__ == "__main__":
    main()
