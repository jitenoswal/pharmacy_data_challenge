
# Table of Contents
1. [What I have built](README.md#what-i-have-built-)
2. [What will be some good additions](README.md#what-will-be-some-good-addition-todos)
3. [Running the application](README.md#running-the-application)
4. [Questions](README.md#questions)

# What I have built :)

1. My implementation is primarily using a dictionary (k: drug_name, v: custom_object) and custom_object (inventoryItem) which I created for this exercies. (custom_object: drug_name, uniq_prescriber_set, total_cost).
2. I have also added essential logging (INFO, ERROR) to make logs useful for monitoring the application. 
3. I have also added error handling which is useful to save the application from edge cases and blowing up to exit. I have raised useful exception whereever necessary. 
4. I have used some OOPs concepts which allows the code to be beautiful (eventhough I'm using Python which makes life easier by being extra user-friendly and gets anyone easily into bad habits)
5. My custom_object has property constraints which enforces the uses of the object to limit themselves to its properties like drug_name & prescriber_name cannot be empty or cost of drug cannot be non float.
6. This was a very good projects making me scratch through some of my python skills as we were dealing with a fairly big dataset (24 million roows) which currently takes around 200ms for my application to generate the results.

# What will be some good additions (TODOs)

1. I feel I would have liked to spend more time on optimizing this solution further by multi-processing or smart-batching my application to run parallelly allowing the application to run on much much larger files but couldn't due to day-time job limitation and less time.
2. I also would have liked to separate my main application file in separate files and then add unit testing module and schema definitions but it would take some more time to tighten those things and I don't want to risk breaking my working application as when you guys run it, I won't have the benefit of physically help run the application if it fails for some reason. 

# Running the application

## Summary

1. As instructed, I have used all basic data-structers and OOPs concept. 
2. Limited use of python packages to pretty basic stuff: logging, os, time, csv. 
3. main() code is in pharmacy-counting.py
4. The application creates a log file when you run it at $output_dir_location/app.log

# Questions?
Email me at jiten.p.oswal@gmail.com
