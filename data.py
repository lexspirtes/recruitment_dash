import pandas as pd

'''this file is for reading data in '''
#reading in data
applicants = pd.read_csv('~/dev/play-dash/applicants.csv')
applicants.last_updated = pd.to_datetime(applicants.last_updated)

#by bootcamp, online, or school                                                                                                                                  
general = applicants.groupby(['is_bootcamp', 'round']).size().to_frame('counts').reset_index()

#by individual school
school_ppl = applicants.loc[applicants.is_bootcamp == 'School']
school_ppl = school_ppl.groupby(['source', 'round']).size().to_frame('counts').reset_index()

#by individual bootcamp
bootcamp_ppl = applicants.loc[applicants.is_bootcamp == 'Bootcamp']
bootcamp_ppl = bootcamp_ppl.groupby(['source', 'round']).size().to_frame('counts').reset_index()
 
