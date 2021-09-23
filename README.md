# airflow-demo

Presentation at https://docs.google.com/presentation/d/1Jdmyw0NX4spOnfQyAPXi-7I7XpZYCe2FHbx1UX8V-gQ/edit?usp=sharing 

The bike trip demo can be found at https://github.com/danielbeach/AirflowVsDagster. It also includes the same pipeline in Dagster, if you're curious.

## Grouparoo-Airflow Demo

This is a very simple airflow DAG that pulls in data from a remote CSV, loads it into a postgres database and triggers Grouparoo by invoking the `grouparoo run` command. Some paths will definitely need to be tweaked to make this work on your local machine.

Included is also the Grouparoo project config used. 

You'll need to create two Connections in airflow:
- Postgres connection to the database you want to load the data into, named `grouparoo_profile_db`
- Discord connection that sets the host to `https://discord.com/api/`, named `discord`.

