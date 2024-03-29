## Production Surveillance Project

> In this I project, I built an oilfield production surveillance dashboard from scratch to deployment. The dashboard monitors changes in wells parameters using data from the oilfield daily reports.

### Architecture Diagram

![](https://github.com/0ladayo/production_surveillance_project/blob/master/Architecture%20Diagram.jpg)

### Languages (Libraries) and Tools Used

#### Google Cloud Storage (GCS)

> google cloud storage (bucket) was used to store the oilfield daily reports

#### Pandas

> pandas library in python was used to access the data in the reports stored in GCS, clean and organize the data in a DataFrame structure and stores the dataframe as an excel file in another google cloud storage bucket

#### Google Cloud Function (GCF)

> google cloud function was used to deploy the data wrangling.py file as a function. This makes the data wrangling.py function to be event driven in response to a trigger (google cloud storage in this case).

#### Plotly 

> plotly library in python was used for the data visualization 

#### Dash

> dash library in python was used to build the interactive web framework.

#### Google App Engine (GAE)

> main.py file was deployed to Google App Engine

### Output

> the output can be viewed via the link below

> [Production Surveillance Dashboard](https://dummy-surveillance-project.nw.r.appspot.com/) 

![](https://github.com/0ladayo/production_surveillance_project/blob/master/web%20app.jpg)

### Note

> because of data privacy policy, the actual wells data have been replaced with randomly generated data

### Blog

> read more here [Building an Oilfield Production Surveillance Dashboard](https://medium.com/@Oladayo/building-an-oilfield-production-surveillance-dashboard-1629865e2ec9) 

> Updates here [Update1](https://medium.com/@Oladayo/update-fa467c737ad4) and here [Update2](https://medium.com/@Oladayo/update-2-5b2340158c8c)

### License

> see the [License](https://github.com/0ladayo/production_surveillance_project/blob/master/LICENSE.txt) file for license rights and limitations (MIT)
