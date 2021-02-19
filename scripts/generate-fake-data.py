from concurrent import futures

import pandas as pd
import random
import os


DATA_CNT = 10000

DEGREES = ['CS', 'MA', 'PSY', 'WR', 'ME', 'IE', 'RBE', 'ECE']
PROBS = {
  'major_2': 0.5,
  'masters': 0.5,
  'phd': 0.1
}

GRAD_YEARS = (1990, 2021)
SALARY_RANGE = (50000, 1e6)

JOB_TITLE = ['Accountant', 'SWE1', 'SWE2', 'SWE3', 'Salesmen']
JOB_DUR_BOUNDS = (1, 10)
COMPANY = ['Pfizer', 'Moderna', 'Raytheon', 'Google', 'Amazon', 'Facebook', 
           'Amazon', 'WPI'] 
LOCATIONS = ['MA', 'CA', 'CT', 'NY', 'MD', 'RI', 'NJ']
SECTORS = ['Big Tech', 'BioTech', 'Automotives', 'Finance', 'Research']

_MAX_JOBS = 4


def generate_person_dict(_):
  person = {}
  person['major'] = random.choice(DEGREES)
  person['grad_year'] = random.randint(*GRAD_YEARS)

  for degree, prob in PROBS.items():
    person[degree] = random.choice(DEGREES) if random.random() < prob else None

  job_cnt = random.randint(1, _MAX_JOBS)
  for i in range(job_cnt):
    job_id = 'job{}'.format(i + 1)
    person[job_id] = random.choice(JOB_TITLE)
    person['{}_tenure'.format(job_id)] = random.randint(*JOB_DUR_BOUNDS)
    person['{}_sector'.format(job_id)] = random.choice(SECTORS)
    person['{}_salary'.format(job_id)] = random.randint(*SALARY_RANGE)

  for i in range(job_cnt, _MAX_JOBS):
    job_id = 'job{}'.format(i + 1)
    person[job_id] = None
    person['{}_tenure'.format(job_id)] = None
    person['{}_sector'.format(job_id)] = None
    person['{}_salary'.format(job_id)] = None

  return person
  

if __name__ == '__main__':
  df = pd.DataFrame(columns=[
    'major', 'major_2', 'masters', 'phd', 'grad_year',
    'job1', 'job1_tenure', 'job1_sector', 'job1_salary',
    'job2', 'job2_tenure', 'job2_sector', 'job2_salary',
    'job3', 'job3_tenure', 'job3_sector', 'job3_salary',
    'job4', 'job4_tenure', 'job4_sector', 'job4_salary',
  ])

  print('Generating data...')
  with futures.ProcessPoolExecutor(max_workers=os.cpu_count() or 2) as exec:
    data = exec.map(generate_person_dict, range(DATA_CNT), chunksize=100)

  print('Writing to file...')
  df = df.append(list(data))

  filename = 'fake-trajectories-{}.csv'.format(DATA_CNT)
  df.to_csv(filename, index_label='id')

  print('Done. Written to {}'.format(filename))