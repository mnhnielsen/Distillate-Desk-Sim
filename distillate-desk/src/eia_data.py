from myeia import API
import pandas as pd

eia = API()

def get_diesel_spot_prices(start_date: str, end_date: str, frequency: str) -> pd.DataFrame:
    """Fetch diesel spot prices from EIA API."""
    
    route = "petroleum/pri/spt"
    id='EER_EPD2DXL0_PF4_Y35NY_DPG'
    df = eia.get_series_via_route(
        route=route,
        series=id,
        frequency=frequency,
        data_identifier="value",
        start_date=start_date,
        end_date=end_date
    )
    
    return df

def get_jetfuel_spot_prices(start_date: str, end_date: str, frequency: str) -> pd.DataFrame:
    """Fetch jet fuel spot prices from EIA API."""
    
    route = "petroleum/pri/spt"
    id = "EER_EPJK_PF4_RGC_DPG"
    df = eia.get_series_via_route(
        route=route,
        series=id,
        frequency=frequency,
        data_identifier="value",
        start_date=start_date,
        end_date=end_date
    )
    return df

def get_distillate_spot_prices(id: str, start_date: str, end_date: str, frequency: str) -> pd.DataFrame:
    """Fetch distillate spot prices from EIA API."""
    route = "petroleum/pri/spt"
    df = eia.get_series_via_route(
        route=route,
        series=id,
        frequency=frequency,
        data_identifier="value",
        start_date=start_date,
        end_date=end_date
    )
    return df