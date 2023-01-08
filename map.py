import pandas as ps
import folium as fo
import webbrowser as wb

def colorize(height):
    if height <= elevation_average / 2:
        return "green"
    elif height <= elevation_average:
        return "orange"
    else:
        return "red"


file = ps.read_excel("VolcanoList.xlsx")
volacone_info = ps.DataFrame(file)

coordinates = volacone_info[["Latitude", "Longitude"]].values.tolist()
name = list(volacone_info["Volcano Name"])
location = list(volacone_info["Country"])
status = list(volacone_info["Last Eruption Year"])
 
elevation = list(volacone_info["Elevation"])
elevation_postive = [i + abs(min(elevation)) for i in elevation]
elevation_sum = sum(elevation_postive)
elevation_normal = [float(i) / elevation_sum for i in elevation_postive]
elevation_average = float(sum(elevation_normal)) / float(len(elevation_normal))


map = fo.Map(
    location=coordinates[0],
    zoom_start=6,
    tiles="Stamen Terrain",
)

fgv = fo.FeatureGroup(name="Volcano Markers")
fgp = fo.FeatureGroup(name="Population Layer")


for cord, el, na, loc, stat, elnorm in zip(
    coordinates, elevation, name, location, status, elevation_normal
):

    fgv.add_child(
        fo.CircleMarker(
            location=cord,
            radius=6,
            popup=f"Height(sealevel)={el} m,\nLast Eruption Year:{stat}",
            tooltip=f"{na}",
            fill_color=colorize(elnorm),
            fill=True,
            fill_opacity=100,
            color="lightgray",
            opacity=2,
        )
    )

fgp.add_child(
    fo.GeoJson(
        data=open("world.json", "r", encoding="utf-8-sig").read(),
        style_function=lambda x: {
            "fillColor": "green"
            if x["properties"]["POP2005"] < 10000000
            else "orange"
            if 10000000 <= x["properties"]["POP2005"] < 20000000
            else "red"
        },
    )
)


map.add_child(fgp)
map.add_child(fgv)
fo.LayerControl().add_to(map)


map.save("Volcano.html")
wb.open_new_tab("Volcano.html")
