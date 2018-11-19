from copy import copy, deepcopy
import Constraint
from IOHandler import IOHandler
import TimeInterval as ti


def restrict_interval(domains, interval: ti.TimeInterval):
    for activity_name, domain in domains.items():
        domains[activity_name] = [x for x in domain if x.day != interval.day or ti.intersect(interval, x) <= 0]


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

    elif not domains[variables[0].name]:
        # Dacă nu mai sunt valori în domeniu, am terminat căutarea
        return False
    elif cost == best_cost:
        # Dacă am ajuns deja la un cost identic cu cel al celei mai bune soluții, nu mergem mai departe
        return False
    else:
        # TODO: Luăm prima variabilă și prima valoare din domeniu
        var = variables[0]
        val = domains[var.name].pop(0)

        # TODO: Construim noua soluție
        new_solution = deepcopy(solution)
        new_solution[var.name] = val
        restrict_interval(domains, val)

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

    input_file = 'input.yml'
    output_file = 'output.yml'

    io_handler = IOHandler(input_file)
    variables, domains, constraints = io_handler.read_yaml()

    best_solution = {}
    best_cost = 999999

    PCSP(variables, deepcopy(domains), constraints, {}, 0)

    print("[FINAL] Best found: " + str(best_cost) + " - " + str(best_solution))


if __name__ == "__main__":
    main()
