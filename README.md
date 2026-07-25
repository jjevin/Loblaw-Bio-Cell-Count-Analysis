# Teiko Technical Assignment - Loblaw Bio Cell Count Analysis

## Instructions for Running

There are three makefile targets, explained below:

``` shell
make setup      # Downloads dependencies from requirements.txt
make pipeline   # Generates the sqlite database and performs all analyses
make dashboard  # Starts the local server for our streamlit dashboard
```

## Database Schema

<!--
An explanation of the schema used for the relational database, with rationale for the design and how this would scale if there were hundreds of projects, thousands of samples and various types of analytics you’d want to perform.
-->

I broke the monolith csv file into three tables:

1. A `projects` table, using the project id as a key and containing all project metadata (in this case, just the sample type).
2. A `subjects` table, using the subject id as a key and containing all subject data (condition, age, sex, treatment, and response). 
3. A `samples` table, containing all keys and the remaining sample-specific information.

This schema minimizes the duplication of project and subject information across the primary samples table. This would reduce the number of update calls required if a change were to be made to any of these tables.

## Code Overview

<!--
A brief overview of your code structure and an explanation of why you designed it the way you did.
-->
This project is laid out as follows:

``` shell
├── cell-count.db     # SQLITE database in project root as requested
├── dashboard.py
├── data/cell-count.csv
├── flake.lock
├── flake.nix
├── load_data.py
├── Makefile
├── modules   # Separate modules used in both pipeline and dashboard
│   ├── b_cell_calculation.py
│   ├── initial_analysis.py
│   ├── statistical_analysis.py
│   ├── subset_analysis.py
│   └── utils.py
├── outputs/    # Sample pipeline outputs generated w/ GitHub action
├── pipeline.py
├── README.md
└── requirements.txt
```

Each analysis point is given its own module since they each follow their own line of research (except the `statistical_analysis` module, which sources `samples_df` from the `initial_analysis` module). The primary responsibility for each of these modules is providing a calculation function, with additional readouts provided when run independently. These are orchestrated by `pipeline.py` and `dashboard.py`, calling each module to either read out the results or embed them in a streamlit dashboard. 

## Dashboard Link

<!-- A link to the dashboard. -->

The dashboard for this project is available [on streamlit](https://fritz-loblaw-bio.streamlit.app/), or can be locally hosted with `streamlit run dashboard.py`. 
