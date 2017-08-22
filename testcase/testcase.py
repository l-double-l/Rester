from logging import getLogger
from rester.exc import TestCaseExec
from rester.http import HttpClient
from rester.loader import TestSuite
import yaml

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


class ApiTestCaseRunner:
    logger = getLogger(__name__)

    def __init__(self, options={}):
        self.options = options
        self.results = []

    def run_test_suite(self, test_suite_file_name):
        test_suite = TestSuite(test_suite_file_name)
        test_suite.load()
        for test in test_suite.test_cases:
            self.run_test_case(test)

    def run_test_case(self, case):
        case.load()
        self._run_case(case)

    def display_report(self):
        for result in self.results:
            if not result['failed']:
                continue
            print("\n\n ############################ FAILED ############################")
            for e in result['failed']:
                print(bcolors.FAIL , result.get('name') , ":" , e['name'])
                print(bcolors.ENDC)
                for i, error in enumerate(e['errors']):
                    print("%d." % i)
                    print(error)
                    print()
                print("-------- LOG OUTPUT --------")
                print(e['logs'])
                print("---------------------------")

        print("\n\n ############################ RESULTS ############################")
        for result in self.results:
            c = bcolors.OKGREEN
            if result.get('failed'):
                c = bcolors.FAIL

            columns = "{0:40}|{1:8}|{2:8}|{3:8}{4:6}"
            row = []
            row.append('{0}{1} '.format(c, result.get('name')))
            for k in ['passed', 'failed', 'skipped']:
                row.append("%s: %d" % (k, len(result.get(k))))
            row.append(bcolors.ENDC)
            print (columns.format(*row))
            #print(c, yaml.dump(result, default_flow_style=False,), bcolors.ENDC

            #self.logger.info("name: {}\n{}\n", name, )
#            test_case = exc.case
#            print("\n\n ===> TestCase : {0}, status : {1}".format(test_case.name, "Passed" if test_case.passed == True else "Failed!")
#            for test_step in test_case.testSteps:
#                #self.logger.info('\n     ====> Test Step name : %s, status : %s, message : %s', test_step.name, test_step.result.status, test_step.result.message)
#                print("\n\n     ====> Test Step : {0}".format(test_step.name)
#
#                if hasattr(test_step, 'result'):
#                    print("\n\n         ====> {0}!".format(test_step.result.message)
#
#                if hasattr(test_step, 'assertResults'):
#                    for assert_result in test_step.assertResults:
#                        #self.logger.debug('\n assert_result : ' + str(assert_result))
#                        print("\n        ---> {0}".format(assert_result['message'])


    def _run_case(self, case):
        tc = TestCaseExec(case, self.options)
        self.results.append(tc())


#TODO
# Support enums
# post processing
