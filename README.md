# plotly-dash-steps

## Usage and purpose
**plotly-dash-steps** is a service with a graphical visualization of measurements from devices for monitoring walking habits and patterns of elderly and disabled persons. 

Service can be accessed from graphical interface via web service.
## Set up the project
### Build new project
1. Build docker image:
```bash
cd docker-base
./build_image.sh
```

### Run project
1. Run docker compose:
```bash
sudo docker-compose up --build
```

## Graphical interface
![Main screen](assets/main_screen.gif?raw=true)
### UI elements
1. **Patient selection dropdown.** Choose patient to observe from dynamically updating list.
2. **Patient bio.** Main information about the patient.
3. **Plot type selection dropdown.** There are 2 plot types avaliable:
    * *History* — plots of the sensors history from the last 10 minutes.
    * *Artifacts* — plots of the sensors artifacts from the last 10 minutes.
4. **Data plot.** Sensors data plot of chosen type. Can be zoomed in a specific x axis range.
5. **Sensor choosing tabs.** Choose sensor to observe, there are 6 options available:
    * *L0* — left foot front sensor.
    * *L1* — left foot middle sensor.
    * *L2* — left foot back sensor.
    * *R0* — right foot front sensor.
    * *R1* — right foot middle sensor.
    * *R2* — right foot back sensor.
6. **Feet visualization.** Feet visuazation with dynamically changing sensors and boxplots, representing metrics of sensors in a chosen date range.