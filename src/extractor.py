import yaml
import argparse
import logging
from jsonschema import validate, ValidationError

# Boilerplate logging code
log_fmt = "%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s"
logging.basicConfig(level=logging.INFO, format=log_fmt)
logger = logging.getLogger(__name__)

# Boilerplate argparser code
argparser = argparse.ArgumentParser(description='Runs Unit Tests for Support Sigma Detections')
argparser.add_argument('-f', '--file', required=True, help='Sigma rule to run unit tests for.')
args = argparser.parse_args()

def parse_sigma(filename: str):
    '''
    Parse Sigma YAML file

    Args:
        filename: filename of Sigma rule
    Returns:
        dict object containing the YAML file
    '''
    with open(filename) as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as e:
            print(e)
            terminate('Error Parsing YAML File')

def get_unit_tests(detection: dict):
    '''
    Get the Unit Tests associated with a detection.

    Args:
        detection (dict): Parsed Sigma file.
    Returns:
        unit-tests (dict): Unit-tests key in the Sigma file.
    '''
    try:
        return detection['unit-tests']['tests']
    except KeyError:
        terminate('unit-tests key not found in Sigma rule.')

def validate_atomic_red_team(atomic_path: str):
    '''
    Validates the Atomic Red Team YAML file for a unit test

    Args:
        path (str): Path to the Atomic Red Team test
    Returns:
        True if valid
        False if invalid
    '''
    # load YAML file for ART test
    with open(atomic_path) as f:
        atomic = yaml.safe_load(f)

    # load the ART schema definition
    with open('./src/utils/atomic-red-team.schema.yaml') as f:
        schema = yaml.safe_load(f)

    try:
        if validate(atomic, schema=schema) == None:
            return True
        else:
            return False
    except:
        terminate(f"Couldn't validate: {atomic_path}")

    #raise NotImplementedError


def terminate(error: str):
    '''
    Print error and terminate script execution
    '''
    logging.error(error)
    exit(1)



if __name__ == '__main__':

    # Read YAML file
    detection = parse_sigma(args.file)

    unit_tests = get_unit_tests(detection)

    for paths in unit_tests:
        validate_atomic_red_team(unit_tests[paths]['path'])