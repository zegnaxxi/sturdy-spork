from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, TimeRemainingColumn

LAT_RANGE = 180.0
LON_RANGE = 360.0

LAT_STEPS = 32
LON_STEPS = 64

def geo_index_to_latlon(geo_index):
    if not (0 <= geo_index <= 2047):
        print("Error: Geo index is out of valid range (0-2047).")
        return None, None

    lat_step_size = LAT_RANGE / LAT_STEPS
    lon_step_size = LON_RANGE / LON_STEPS

    lat_idx = geo_index // LON_STEPS
    lon_idx = geo_index % LON_STEPS

    latitude_center = -LAT_RANGE/2 + (lat_idx * lat_step_size) + (lat_step_size / 2)
    longitude_center = -LON_RANGE/2 + (lon_idx * lon_step_size) + (lon_step_size / 2)

    return latitude_center, longitude_center

def latlon_to_geo_index(latitude, longitude):
    if not (-LAT_RANGE/2 <= latitude <= LAT_RANGE/2) or not (-LON_RANGE/2 <= longitude <= LON_RANGE/2):
        print("Error: Latitude or longitude is out of valid range.")
        return None

    lat_step_size = LAT_RANGE / LAT_STEPS
    lon_step_size = LON_RANGE / LON_STEPS

    lat_idx = int((latitude + 90.0) / lat_step_size)
    if lat_idx >= LAT_STEPS:
        return None
        lat_idx = LAT_STEPS - 1

    lon_idx = int((longitude + 180.0) / lon_step_size)
    if lon_idx >= LON_STEPS:
        return None

    geo_index = lat_idx * LON_STEPS + lon_idx
    return geo_index

def test_inverse():
    # Define the columns you want in your progress bar.
    # rich offers a lot of flexibility here!
    with Progress(
        TextColumn("[progress.description]{task.description}"), # Description text
        BarColumn(),                                      # The progress bar itself
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"), # Percentage complete
        TimeElapsedColumn(),                              # Time elapsed since start
        TimeRemainingColumn(),                            # Estimated time remaining
        # You can add more, like MofNCompleteColumn for "X/Y complete"
    ) as progress:
        # Add a task to the progress bar. This is how rich manages individual bars.
        # total=2048 tells rich the total number of steps for this task.
        task = progress.add_task("[green]Testing Geo Index Conversion...", total=2048)

        for i in range(2048):
            lat, lon = geo_index_to_latlon(i)
            geo_index = latlon_to_geo_index(lat, lon)

            if geo_index != i:
                # Use console.print() to output the error message without breaking
                # the rich progress bar's display.
                progress.console.print(f"[red]Fail: index {i} -> latitude: {lat}, longitude: {lon}, recalculated index: {geo_index}[/red]")
                # If you want to stop the progress bar immediately on failure:
                progress.stop()
                return

            # Advance the progress bar for the current task by 1 step.
            progress.update(task, advance=1)
            # You can uncomment this line to simulate work and see the bar in action
            # time.sleep(0.001)
