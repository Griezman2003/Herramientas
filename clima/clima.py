import requests
from datetime import datetime

def get_wind_direction(degrees):
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    idx = int((degrees + 22.5) // 45)
    return directions[idx]

def format_time_iso(time_iso):
    dt = datetime.fromisoformat(time_iso)
    return dt.strftime('%I:%M %p').lstrip('0').lower()

def format_sun_time(time_iso):
    dt = datetime.fromisoformat(time_iso)
    return dt.strftime('%I:%M %p').lstrip('0').lower()

def format_date(date_iso):
    dt = datetime.fromisoformat(date_iso)
    return dt.strftime('%a, %d %b')

def get_location_by_ip():
    try:
        response = requests.get("http://ip-api.com/json/", timeout=5)
        data = response.json()
        if data.get("status") != "success":
            print(f"⚠️ No se pudo obtener la ubicación: {data.get('message')}")
            return None

        return {
            "lat": data["lat"],
            "lon": data["lon"],
            "city": f"{data['city']}, {data['regionName']}"
        }

    except Exception as e:
        print("⚠️ Error al obtener ubicación automáticamente:", e)
        return None

def main():
    location = get_location_by_ip()
    lat = location["lat"]
    lon = location["lon"]
    city_name = location["city"]

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&"
        f"current_weather=true&"
        f"hourly=temperature_2m,precipitation_probability,weathercode,uv_index&"
        f"daily=temperature_2m_max,temperature_2m_min,precipitation_sum,sunrise,sunset&"
        f"timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        current = data.get('current_weather', {})
        temp_c = current.get('temperature')
        wind_speed = current.get('windspeed')
        wind_dir_deg = current.get('winddirection')
        weather_code = current.get('weathercode')
        time_iso = current.get('time')
        wind_dir = get_wind_direction(wind_dir_deg) if wind_dir_deg is not None else 'N/A'

        daily = data.get('daily', {})
        dates = daily.get('time', [])
        temp_maxs = daily.get('temperature_2m_max', [])
        temp_mins = daily.get('temperature_2m_min', [])
        precipitation_sums = daily.get('precipitation_sum', [])
        sunrises = daily.get('sunrise', [])
        sunsets = daily.get('sunset', [])

        hourly = data.get('hourly', {})
        precipitation_prob = hourly.get('precipitation_probability', [0])[0]
        uv_index = hourly.get('uv_index', [0])[0]

        weather_conditions = {
            0: "Despejado",
            1: "Parcialmente nublado",
            2: "Nublado",
            3: "Nublado",
            45: "Neblina",
            48: "Neblina helada",
            51: "Llovizna ligera",
            53: "Llovizna moderada",
            55: "Llovizna fuerte",
            61: "Lluvia ligera",
            63: "Lluvia moderada",
            65: "Lluvia fuerte",
            71: "Nieve ligera",
            73: "Nieve moderada",
            75: "Nieve fuerte",
            80: "Chubascos ligeros",
            81: "Chubascos moderados",
            82: "Chubascos fuertes",
            95: "Tormenta eléctrica",
            99: "Tormenta eléctrica severa"
        }

        condition_desc = weather_conditions.get(weather_code, "Desconocido")

        print(f"📍 Ubicación: {city_name}")
        print(f"🕒 Hora reporte: {format_time_iso(time_iso)}")
        print(f"🌡️ Temperatura actual: {temp_c} °C (Máx: {temp_maxs[0]} °C / Mín: {temp_mins[0]} °C)")
        print(f"🌥️ Condición: {condition_desc}")
        print(f"🌧️ Precipitación total hoy: {precipitation_sums[0]} mm")
        print(f"💧 Probabilidad de lluvia (hora actual): {precipitation_prob} %")
        print(f"☀️ Índice UV: {uv_index}")
        print(f"💨 Viento: {wind_speed} km/h dirección {wind_dir} ({wind_dir_deg}°)")
        print(f"🌅 Amanecer: {format_sun_time(sunrises[0])}")
        print(f"🌇 Atardecer: {format_sun_time(sunsets[0])}")

        if precipitation_prob > 50:
            print("⚠️ Alta probabilidad de lluvia, considera llevar paraguas.")
        if wind_speed > 50:
            print("⚠️ Viento fuerte, toma precauciones.")

        print("\n📅 Pronóstico extendido (5 días):")
        for i in range(min(5, len(dates))):
            date_fmt = format_date(dates[i])
            temp_max = temp_maxs[i]
            temp_min = temp_mins[i]
            precip = precipitation_sums[i]
            sunrise_fmt = format_sun_time(sunrises[i])
            sunset_fmt = format_sun_time(sunsets[i])
            print(f"{date_fmt}: Máx {temp_max}°C / Mín {temp_min}°C, Precipitación: {precip} mm, 🌅 {sunrise_fmt} / 🌇 {sunset_fmt}")

    except requests.exceptions.RequestException as e:
        print("❌ Error de conexión o respuesta inválida:", e)

if __name__ == "__main__":
    main()
