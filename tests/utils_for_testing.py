from argparse import Namespace


def mockify_dict(dict_data):
    """ Used to create a mock object """
    return Namespace(**dict_data)
