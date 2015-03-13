from sys import version_info


def get_input(prompt):
    if version_info >= (3, 0):
        return input(prompt)
    else:
        return raw_input(prompt)
