# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium.common.exceptions import ElementClickInterceptedException
#NoSuchElementException,StaleElementReferenceException
from selenium import webdriver
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path ,location, sleep_time):

    '''Gathers jobs as a dataframe, scraped from Glassdoor'''

    #Initializing the webdriver
    options = webdriver.ChromeOptions()

    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')

    #Change the path to where chromedriver is in your home folder.
    driver = webdriver.Chrome(executable_path=path, options=options)
    driver.set_window_size(1000, 800)

    #url = 'https://glassdoor.co.in/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword="'+ location +'"&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    #url = 'https://www.glassdoor.co.in/Job/jobs.htm?sc.generalKeyword=%22'+ keyword +'%22&sc.locationSeoString='+ location +'&locId=1&locT=N'
    url = 'https://www.glassdoor.co.in/Job/'+ location +'-'+ keyword +'-jobs-SRCH_IL.0,2_IN1_KO3,17.htm'
            
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(sleep_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
            #driver.find_element_by_class_name("ModalStyle__xBtn___29PT9").click()  #clicking to the X.
            driver.find_element_by_css_selector('[alt=Close]').click()  #clicking to the X.
            print("X clicked worked")
        #except NoSuchElementException:
        except Exception as e:
            print("X clicked failed, Exception: " + str(e))
            pass


        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("jl")  #jl for Job Listing. These are the buttons we're going to click.
        print('job_buttons length :' + str(len(job_buttons)))
        
        for job_button in job_buttons:
            
            #with open('job_button_file.txt','a+') as file:
                #file.write('\n')
                #file.write(job_button.get_attribute('innerHTML'))
                #file.write('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
                #file.write('\n')
            
            print('Entry into for loop')

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                print('break happened')
                break
            
            try:
                time.sleep(5)
                job_button.click()  #You might
                time.sleep(3)
            except Exception:
                print('passed - ElementClickInterceptedException: element click intercepted:')
                continue
                
            print('sleep done')
            
            try:
                company_name = driver.find_element_by_xpath('.//div[@class="employerName"]').text
            #except NoSuchElementException:
            except Exception as e:
                company_name = '-1 Exception: {' + str(e) +'}'
                
            try:
                location = driver.find_element_by_xpath('.//div[@class="location"]').text
            #except NoSuchElementException:
            except Exception as e:
                location = '-1 Exception: {' + str(e) +'}'
            
            try:
                job_title = driver.find_element_by_xpath('.//div[contains(@class, "title")]').text
            #except NoSuchElementException:
            except Exception as e:
                job_title = '-1 Exception: {' + str(e) +'}'
            
            try:
                job_description = driver.find_element_by_xpath('.//div[@class="jobDescriptionContent desc"]').text
            #except NoSuchElementException:
            except Exception as e:
                job_description = '-1 Exception: {' + str(e) +'}'
            
            print('initial done')

            try:
                salary_estimate = driver.find_element_by_xpath('.//li[@class="jl react-job-listing gdGrid selected"]//span[@class="gray salary"]').text
            #except NoSuchElementException:
                #salary_estimate = -1 #You need to set a "not found value. It's important."
            except Exception as e:
                salary_estimate = '-1 Exception: {' + str(e) +'}'

            try:
                rating = driver.find_element_by_xpath('.//span[@class="rating"]').text
            #except NoSuchElementException:
                #rating = -1 #You need to set a "not found value. It's important."
            except Exception as e:
                rating = '-1 Exception: {' + str(e) +'}'
            
            print('initial-2 done')
            
            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>
            try:
                driver.find_element_by_xpath('.//div[@class="tab" and @data-tab-type="overview"]').click()

                try:
                    #<div class="infoEntity">
                    #    <label>Headquarters</label>
                    #    <span class="value">San Francisco, CA</span>
                    #</div>
                    headquarters = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Headquarters"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    headquarters = '-1 Exception: {' + str(e) +'}'

                try:
                    size = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Size"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    size = '-1 Exception: {' + str(e) +'}'

                try:
                    founded = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Founded"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    founded = '-1 Exception: {' + str(e) +'}'

                try:
                    type_of_ownership = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Type"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    type_of_ownership = '-1 Exception: {' + str(e) +'}'

                try:
                    industry = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Industry"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    industry = '-1 Exception: {' + str(e) +'}'

                try:
                    sector = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Sector"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    sector = '-1 Exception: {' + str(e) +'}'

                try:
                    revenue = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Revenue"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    revenue = '-1 Exception: {' + str(e) +'}'

                try:
                    competitors = driver.find_element_by_xpath('.//div[@class="infoEntity"]//label[text()="Competitors"]//following-sibling::*').text
                #except NoSuchElementException:
                except Exception as e:
                    competitors = '-1 Exception: {' + str(e) +'}'
                    

            #except NoSuchElementException:  #Rarely, some job postings do not have the "Company" tab.
            except Exception as e:  #Rarely, some job postings do not have the "Company" tab.
                headquarters = '-1 Exception: {' + str(e) +'}'
                size = '-1 Exception: {' + str(e) +'}'
                founded = '-1 Exception: {' + str(e) +'}'
                type_of_ownership = '-1 Exception: {' + str(e) +'}'
                industry = '-1 Exception: {' + str(e) +'}'
                sector = '-1 Exception: {' + str(e) +'}'
                revenue = '-1 Exception: {' + str(e) +'}'
                competitors = '-1 Exception: {' + str(e) +'}'


            if verbose:
                print("Headquarters: {}".format(headquarters))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("Competitors: {}".format(competitors))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            print('initial-3 done')
            
            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Headquarters" : headquarters,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue,
            "Competitors" : competitors})
            #add job to jobs

        print('Done till here')

        #Clicking on the "next page" button
        try:
            driver.find_element_by_xpath('.//li[@class="next"]//a').click()
        except Exception as e:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)) + ' Exception: '+ str(e))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.


