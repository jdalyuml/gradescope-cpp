import subprocess
import json
import yaml

class CppTest:
    def __init__(self, data:dict):
        self.data = data
        self.msg = self.data['desc']
        self.prog = self.data['program']
        self.timeout = 60 # seconds

    def _compile(self):
        process = subprocess.run([f'make -f MakefileProf.mak {self.prog}.test'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, timeout=self.timeout)
        if process.returncode:
            self.msg += ''.join(c for c in process.stdout)
        return process.returncode == 0

    def _execute(self):
        process = subprocess.run([f'./{self.prog}.test'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True, text=True, timeout=self.timeout)
        if process.returncode:
            self.msg += ''.join(c for c in process.stdout)
        return process.returncode == 0
    
    def Run(self):
        self.passed = self._compile() and self._execute()

    def ToJson(self):
        obj = {k:v for k,v in self.data.items()}
        obj['max_score'] = self.data['weight']
        if 'name' not in obj:
            obj['name'] = self.prog
        if self.passed:
            obj['status'] = 'passed'
            obj['score'] = obj['max_score']
        else:
            obj['status'] = 'failed'
            obj['score'] = 0
        obj['output'] = self.msg
        obj['output_format'] = 'ansi'
        return json.dumps(obj)

def RunFile(filename, outfile):
    import sys
    with open(filename, 'r') as fin:
        tests = yaml.safe_load(fin)
        
    with open (outfile, 'w') as fout:
        for testData in tests:
            test = CppTest(testData)
            test.Run()
            fout.write(test.ToJson())
            fout.write('\n')
            # print(test.ToJson())

RunFile('Tests.yaml', '/autograder/results/cpptests.json')