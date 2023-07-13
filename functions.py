# additional functions
def ok_module_info(name):
    print(f"{name} - OK")


def error_module_info(name):
    print(f"No such module as {name}")
    print(f"Install module using 'pip install {name}' command.")
    print("--------------------------------------")


def get_horizon_data(nasaids, names, colors, sizes, start_date="2018-01-01"):
    """nasaids = [1, 2, 3, 4]
    function inspired by project https://github.com/chongchonghe/Python-solar-system"""

    from astropy.time import Time
    from astroquery.jplhorizons import Horizons
    from numpy import double

    data = {
        "info": "Database about position and speed planets",
        "date": start_date,
    }

    for i, nasaid in enumerate(nasaids):
        obj = Horizons(id=nasaid, location="@sun", epochs=Time(start_date).jd, id_type="id").vectors()
        print("-----------------------------------------------------------------------")
        print(f"Downloading data for {names[i]}:")
        print(obj)

        data[nasaid] = {
            "name": names[i],
            "size": sizes[i],
            "color": colors[i],
            "r": [double(obj[xi]) for xi in ["x", "y", "z"]],
            "v": [double(obj[vxi]) for vxi in ["vx", "vy", "vz"]],
        }
    return data


if __name__ == "__main__":
    print("It is additional functions.")
