## Production Surveillance Project

> In this I project, I built an oilfield production surveillance dashboard from scratch to deployment. The dashboard monitors changes in wells parameters using data from the oilfield daily reports.

### Languages (Libraries) and Tools Used

#### Google Cloud Storage (GCS)

> google cloud storage bucket was used to store the oilfield daily reports

#### Pandas

> pandas library in python was used to access the data in the reports stored in GCS, clean and organize the data in a DataFrame structure and stores the dataframe as an excel file in another google cloud storage bucket

#### Google Cloud Function (GCF)

> google cloud function was used to deploy the data wrangling.py file. This makes the data wrangling.py function to be event driven in response to a trigger (google cloud storage in this case).

#### Plotly 

> plotly library in python was used for the data visualization 

#### Dash

> dash library in python was used to build the interactive web framework.

#### Google App Engine (GAE)

> google app engine was used to deploy the main.py file.

### Final Output

> the final output can be see via the link below

> [Production Surveillance Dashboard](https://dummy-surveillance-project.nw.r.appspot.com/) 

### Note

> because of data privacy policy, the actual wells data and names have been replaced with randomly generated data
