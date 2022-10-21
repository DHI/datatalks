# Data Talk 12: Quickly turn python scripts into apps with Streamlit

*Clemens Cremer & Paul Daniel, October 27.*

Do you sometimes feel you could use and present your python work more efficiently as an app? For instance to quickly prototype a tool to discuss and narrow down requirements in further development or to provide access to your tools for non-python users?
 
As an engineer (at DHI) there is a good chance you might be well versed in scripting (especially when joining data talks).
However, you might lack experience in front-end development and associated frameworks (such as React, Svelte or Angular), needed to convert your scripts to apps.

Streamlit provides a very simple way to deploy pure python code as (web)app. 
This can, for instance, assist you in tool development phases with frequent iterations. 

Originating from ML Pipelining, streamlit has seen huge adoption and matured throughout the last years. And can pose an alternative to full fledged app development.

In this Data Talk we give a short overview of streamlit and present a practical example from timeseries outlier detection and machine-learning workflow.

## Why?

Why would you want to create webapps?  

* Develop webapps as byproduct of scripting and enable broader use
* Visual representation  
    * facilitates understanding from a user perspective
    * helps in getting feedback
    * helps to manage requirements
* Minimum distance between development and "final" product
    * makes it very fast and easy to iterate (try ideas, manage requirements)
* Communication not by changing variables (e.g. filenames) in a script but interactively (e.g. drag and drop file) 
* Going from experiments to production, facilitating fast iterations in small teams e.g. without handover from backend to frontend teams


## From python scripts to webapps in minutes

Streamilt apps can be deployed in many ways for example

* Streamlit Cloud
* Azure WebApps
* ...

## Useful resources 

1. [Turn Python Scripts into Beautiful ML Tools](https://towardsdatascience.com/coding-ml-tools-like-you-code-ml-models-ddba3357eace)
2. [Useful features in streamlit](https://towardsdatascience.com/10-features-your-streamlit-ml-app-cant-do-without-implemented-f6b4f0d66d36)
3. [Streamlit gallery](https://streamlit.io/gallery)
