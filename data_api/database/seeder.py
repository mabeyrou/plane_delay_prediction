import pandas as pd
from sqlalchemy.orm import Session
from database.engine import SessionLocal, engine, Base
from typing import Dict
from loguru import logger
from os.path import join
from models.airline import Airline
from models.airport import Airport
from models.flight import Flight


class DataSeeder:
    COLS_TO_KEEP = [
        "YEAR",
        "QUARTER",
        "MONTH",
        "DAY_OF_MONTH",
        "DAY_OF_WEEK",
        "FL_DATE",
        "UNIQUE_CARRIER",
        "AIRLINE_ID",
        "CARRIER",
        "TAIL_NUM",
        "FL_NUM",
        "ORIGIN_AIRPORT_ID",
        "ORIGIN_AIRPORT_SEQ_ID",
        "ORIGIN_CITY_MARKET_ID",
        "ORIGIN",
        "ORIGIN_CITY_NAME",
        "ORIGIN_STATE_ABR",
        "ORIGIN_STATE_FIPS",
        "ORIGIN_STATE_NM",
        "ORIGIN_WAC",
        "DEST_AIRPORT_ID",
        "DEST_AIRPORT_SEQ_ID",
        "DEST_CITY_MARKET_ID",
        "DEST",
        "DEST_CITY_NAME",
        "DEST_STATE_ABR",
        "DEST_STATE_FIPS",
        "DEST_STATE_NM",
        "DEST_WAC",
        "CRS_DEP_TIME",
        "DEP_TIME",
        "DEP_DELAY",
        "DEP_DELAY_NEW",
        "DEP_DEL15",
        "DEP_DELAY_GROUP",
        "DEP_TIME_BLK",
        "TAXI_OUT",
        "WHEELS_OFF",
        "WHEELS_ON",
        "TAXI_IN",
        "CRS_ARR_TIME",
        "ARR_TIME",
        "ARR_DELAY",
        "ARR_DELAY_NEW",
        "ARR_DEL15",
        "ARR_DELAY_GROUP",
        "ARR_TIME_BLK",
        "CANCELLED",
        "DIVERTED",
        "CRS_ELAPSED_TIME",
        "ACTUAL_ELAPSED_TIME",
        "AIR_TIME",
        "FLIGHTS",
        "DISTANCE",
        "DISTANCE_GROUP",
    ]

    def __init__(self, db: Session):
        self.db = db

    def load_csv_data(self, csv_path: str) -> pd.DataFrame:
        """Charge les données du CSV"""
        try:
            df = pd.read_csv(csv_path)
            logger.info(f"Données chargées : {len(df)} lignes")
            return df
        except Exception as e:
            logger.error(f"Erreur lors du chargement du CSV : {e}")
            raise

    def seed_airlines(self, df: pd.DataFrame) -> Dict[str, int]:
        try:
            unique_airline = df[["UNIQUE_CARRIER", "AIRLINE_ID"]].drop_duplicates()

            airline_mapping = {}

            existing_airlines = self.db.query(Airline).all()
            existing_names = {a.unique_carrier: a.id for a in existing_airlines}

            airlines_to_insert = []

            for _, row in unique_airline.iterrows():
                unique_carrier = row["UNIQUE_CARRIER"]

                if unique_carrier in existing_names:
                    airline_mapping[unique_carrier] = existing_names[unique_carrier]
                else:
                    new_airline = Airline(
                        unique_carrier=unique_carrier,
                        airline_id=row["AIRLINE_ID"],
                    )
                    airlines_to_insert.append(new_airline)

            if airlines_to_insert:
                self.db.add_all(airlines_to_insert)
                self.db.flush()

                for airline in airlines_to_insert:
                    airline_mapping[airline.unique_carrier] = airline.id

            self.db.commit()
            logger.info(f"Dimension airlines peuplée : {len(airline_mapping)} airlines")

            return airline_mapping

        except Exception as e:
            self.db.rollback()
            logger.error(f"Erreur lors du peuplement des compagnies aériennes : {e}")
            raise
        finally:
            self.db.close()

    def seed_airports(self, df: pd.DataFrame) -> Dict[str, int]:
        try:
            origin_mapping = {
                "ORIGIN": "iata_code",
                "ORIGIN_AIRPORT_ID": "airport_tech_id",
                "ORIGIN_AIRPORT_SEQ_ID": "airport_seq_id",
                "ORIGIN_CITY_MARKET_ID": "city_market_id",
                "ORIGIN_CITY_NAME": "city_name",
                "ORIGIN_STATE_ABR": "state_abr",
                "ORIGIN_STATE_FIPS": "state_fips",
                "ORIGIN_STATE_NM": "state_name",
                "ORIGIN_WAC": "wac_code",
            }

            dest_mapping = {
                k.replace("ORIGIN", "DEST"): v for k, v in origin_mapping.items()
            }

            origin_cols = list(origin_mapping.keys())
            dest_cols = list(dest_mapping.keys())

            origin_df = df[origin_cols].rename(columns=origin_mapping)
            dest_df = df[dest_cols].rename(columns=dest_mapping)

            all_unique_airports = pd.concat(
                [origin_df, dest_df], ignore_index=True
            ).drop_duplicates()

            airport_mapping = {}

            existing_airport = self.db.query(Airport).all()
            existing_codes = {a.iata_code: a.id for a in existing_airport}

            airports_to_insert = []

            for _, row in all_unique_airports.iterrows():
                iata_code = row["iata_code"]

                if iata_code in existing_codes:
                    airport_mapping[iata_code] = existing_codes[iata_code]
                else:
                    new_airport = Airport(
                        iata_code=iata_code,
                        airport_tech_id=row["airport_tech_id"],
                        airport_seq_id=row["airport_seq_id"],
                        city_market_id=row["city_market_id"],
                        city_name=row["city_name"],
                        state_abr=row["state_abr"],
                        state_fips=row["state_fips"],
                        state_name=row["state_name"],
                        wac_code=row["wac_code"],
                    )
                    airports_to_insert.append(new_airport)

            if airports_to_insert:
                self.db.add_all(airports_to_insert)
                self.db.flush()

                for airport in airports_to_insert:
                    airport_mapping[airport.iata_code] = airport.id

            self.db.commit()
            logger.info(
                f"Dimension aéroports peuplée : {len(airport_mapping)} aéroports"
            )

            return airport_mapping

        except Exception as e:
            self.db.rollback()
            logger.error(f"Erreur lors du peuplement des compagnies aériennes : {e}")
            raise
        finally:
            self.db.close()

    def seed_flights(self, df: pd.DataFrame, airline_mapping, airport_mapping) -> None:
        try:
            flights_to_insert = []

            # airline_mapping = {
            #     a.unique_carrier: a.id for a in self.db.query(Airline).all()
            # }

            # airport_mapping = {a.iata_code: a.id for a in self.db.query(Airport).all()}

            for _, row in df.iterrows():
                airline_id = airline_mapping.get(row["UNIQUE_CARRIER"])
                origin_id = airport_mapping.get(row["ORIGIN"])
                dest_id = airport_mapping.get(row["DEST"])

                if airline_id is None or origin_id is None or dest_id is None:
                    logger.warning(f"Relation manquante pour la ligne {row.to_dict()}")
                    continue

                flight = Flight(
                    origin_airport_id=origin_id,
                    dest_airport_id=dest_id,
                    airline_id=airline_id,
                    day_of_week=row["DAY_OF_WEEK"],
                    day_of_month=row["DAY_OF_MONTH"],
                    month=row["MONTH"],
                    year=row["YEAR"],
                    quarter=row["QUARTER"],
                    fl_date=row["FL_DATE"],
                    tail_num=row["TAIL_NUM"],
                    fl_num=row["FL_NUM"],
                    crs_dep_time=row["CRS_DEP_TIME"],
                    dep_time=row["DEP_TIME"],
                    dep_delay=row["DEP_DELAY"],
                    dep_delay_new=row["DEP_DELAY_NEW"],
                    dep_del15=row["DEP_DEL15"],
                    dep_delay_group=row["DEP_DELAY_GROUP"],
                    dep_time_blk=row["DEP_TIME_BLK"],
                    taxi_out=row["TAXI_OUT"],
                    wheels_off=row["WHEELS_OFF"],
                    wheels_on=row["WHEELS_ON"],
                    taxi_in=row["TAXI_IN"],
                    crs_arr_time=row["CRS_ARR_TIME"],
                    arr_time=row["ARR_TIME"],
                    arr_delay=row["ARR_DELAY"],
                    arr_delay_new=row["ARR_DELAY_NEW"],
                    arr_delay_group=row["ARR_DELAY_GROUP"],
                    arr_time_blk=row["ARR_TIME_BLK"],
                )
                flights_to_insert.append(flight)

            if flights_to_insert:
                self.db.add_all(flights_to_insert)
                self.db.commit()
                logger.info(
                    f"{len(flights_to_insert)} vols insérés dans la table centrale."
                )

        except Exception as e:
            self.db.rollback()
            logger.error(f"Erreur lors du peuplement des vols : {e}")
            raise
        finally:
            self.db.close()

    def clean_data(self, csv_path: str) -> pd.DataFrame:
        df = pd.read_csv(csv_path, usecols=self.COLS_TO_KEEP)
        df = df.dropna()
        return df

    def seed_from_csv(self, csv_path: str, batch_size: int = 1000) -> None:
        df = self.clean_data(csv_path)

        airline_mapping = self.seed_airlines(df)
        airport_mapping = self.seed_airports(df)
        self.seed_flights(
            df, airline_mapping=airline_mapping, airport_mapping=airport_mapping
        )


def init_db():
    """Initialise la base de données"""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized!")


def main():
    init_db()

    try:
        with SessionLocal() as db:
            seeder = DataSeeder(db)
            # boucler sur tous les datasets
            csv_path = join("data", "raw", "2016_01.csv")
            batch_size = 1000

            seeder.seed_from_csv(csv_path, batch_size)
    except Exception as err:
        logger.error(f"Seeding failed: {str(err)}")
        raise


if __name__ == "__main__":
    main()
