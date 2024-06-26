import datetime
from services.users.entities.user import User
from ..entities.bulletin import Bulletin
from psycopg2 import extras

from database.base_model import BaseModel

from services.users.models.user_model import UserModel
from services.zones.models.zone_model import ZoneModel
from services.zones.entities.zone import Zone
from services.utils.payment_methods import PaymentMethod

from database.db_connection import get_connection

class BulletinModel(BaseModel):
    @classmethod
    def get_bulletins(cls, interval: tuple= (0, 50), **kwargs) -> list[dict]:
        result = cls.get_elements("bulletins", interval, **kwargs)
        bulletins: list[Bulletin] = []

        for bulletin in result:
            # Creating bulletins object from database bulletins data
            responsible: User = UserModel.get_user(bulletin["responsible_id"])
            zone: Zone = ZoneModel.get_zone(bulletin["zone_id"])
            payment_method: PaymentMethod = PaymentMethod.get_enum_value(bulletin["payment_method"])

            bulletins.append(
                Bulletin(
                    id = bulletin["id"],
                    responsible = responsible,
                    zone = zone,
                    duration = bulletin.get("duration"),
                    registration = bulletin["registration"],
                    precept = bulletin["precept"],
                    price = bulletin.get("price"),
                    payment_method = payment_method,
                    paid = bulletin.get("paid"),
                    created_at = bulletin["created_at"],
                    brand = bulletin.get("brand"),
                    model = bulletin.get("model"),
                    color = bulletin.get("color")
                ).to_json()
            )

        return bulletins

    @classmethod
    def get_similar_bulletins(cls, registration: str) -> list[dict]:

        # Return a maximum of 50 elements
        interval: tuple= (0, 50)

        if registration is None or len(registration) == 0:
            return []
        
        """  if len(registration) < 3:
            return cls.get_bulletins(interval, **kwargs)
        """
        
        bulletins: list[Bulletin] = []
        
        limit = interval[1] - interval[0]
        offset = interval[0]
        
        query = f'''
                SELECT * FROM bulletins 
                WHERE registration LIKE %s
                AND paid = 'false'
                LIMIT %s OFFSET %s 
            '''

        values = (f'%{registration}%', limit, offset)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, values)

            result = cursor.fetchall()

            for bulletin in result:
                # Creating bulletins object from database bulletins data
                responsible: User = UserModel.get_user(bulletin["responsible_id"])
                zone: Zone = ZoneModel.get_zone(bulletin["zone_id"])
                payment_method: PaymentMethod = PaymentMethod.get_enum_value(bulletin["payment_method"])

                bulletins.append(
                    Bulletin(
                        id = bulletin["id"],
                        responsible = responsible,
                        zone = zone,
                        duration = bulletin.get("duration"),
                        registration = bulletin["registration"],
                        precept = bulletin["precept"],
                        price = bulletin.get("price"),
                        payment_method = payment_method,
                        paid = bulletin.get("paid"),
                        created_at = bulletin["created_at"],
                        brand = bulletin.get("brand"),
                        model = bulletin.get("model"),
                        color = bulletin.get("color")
                    ).to_json()
                )
            cursor.close()
            conn.close()
            
        except Exception as exception:
            print(exception)
            return None

        return bulletins


    @classmethod
    def get_bulletin(cls, id:str) -> Bulletin|None:
        """
            Returns a bulletin object with the data saved on the database for the introduced id.
            Returns None if the bulletin id doesn't exists
        """
        result = cls.get_element('bulletins', id)
        
        if (result == None):
            return None

        responsible: User = UserModel.get_user(result["responsible_id"])
        zone: Zone = ZoneModel.get_zone(result["zone_id"])

        payment_method = result.get("payment_method", None)
        payment_method_obj: PaymentMethod = None

        if payment_method is not None:
            payment_method_obj = PaymentMethod(payment_method)

        
        return Bulletin(
            id = result["id"],
            responsible = responsible, 
            zone = zone, 
            duration = result.get("duration"), 
            registration = result["registration"], 
            precept = result["precept"],
            price = result.get("price"), 
            payment_method= payment_method_obj,
            paid = result.get("paid", False), 
            created_at = result["created_at"],
            brand = result.get("brand"), 
            model = result.get("model"), 
            color = result.get("color") 
        )
    
    @classmethod
    def count_bulletins(cls, **kwargs) -> int:
        return cls.count_elements("bulletins", **kwargs)

    @classmethod
    def create_bulletin(self, 
                responsible: User, 
                zone: Zone,
                registration: str,
                precept: str,
                created_at:datetime.datetime = datetime.datetime.now(),
                brand: str = None,
                model: str = None,
                color: str = None
            ) -> Bulletin:
        
        """Create a bulletin and returns the created Bulletin if it is successfully created."""

        bulletin: Bulletin
        zone_bulletins_amount = ZoneModel.count_bulletin(zone.id)
        
        if(zone_bulletins_amount < 0):
            return None;

        id = f"{zone.identifier}/{str(zone_bulletins_amount).zfill(5)}"

        
        query = '''
                INSERT INTO bulletins(id, responsible_id, zone_id, registration,
                    precept, brand, model, color, created_at) 
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s) 
                RETURNING *
            '''

        values = (id, responsible.id, zone.id, registration, precept, brand, model, color, created_at)

        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, values)

            
            result = cursor.fetchone()
            
            bulletin: Bulletin = Bulletin(
                id = result["id"],
                responsible =responsible, 
                zone = zone,
                registration = result["registration"],
                precept = result["precept"],
                created_at = result["created_at"],
                brand = result.get("brand"), 
                model = result.get("model"), 
                color = result.get("color")
            )

            
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as exception:
            print(exception)
            return None
        
        return bulletin
    
    @classmethod
    def delete_bulletin(cls, id: int) -> Bulletin:
        """
            Delete the bulletin with params id and returns it.
            Returns an exception if it is not found.
        """

        deleted_bulletin:Bulletin = cls.get_bulletin(id)
        try:
            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute('DELETE FROM bulletins WHERE id = %s', (id,))
            conn.commit()
            conn.close()
        except Exception as exception:
            return None

        return deleted_bulletin


    @classmethod
    def pay_bulletin(cls, bulletin_id:int, payment_method: PaymentMethod, price: str, duration: str) -> Bulletin:
        updated_bulletin: Bulletin

        bulletin: Bulletin = cls.get_bulletin(bulletin_id)
        if bulletin.paid:
            raise Exception("El boletín introducido ya ha sido pagado")


        query = '''
            UPDATE bulletins SET paid = true, payment_method = %s, price = %s, duration = %s
            WHERE id = %s
            RETURNING *
        '''
        
        try:

            conn = get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)
            cursor.execute(query, (payment_method.value, price, duration, bulletin_id))
            result = cursor.fetchone()

            # Creating bulletin object from database bulletin data
            responsible: User = UserModel.get_user(result["responsible_id"])
            zone: Zone = ZoneModel.get_zone(result["zone_id"])
            payment_method: PaymentMethod = PaymentMethod(result["payment_method"])


            updated_bulletin = Bulletin(
                id = result["id"],
                responsible = responsible, 
                zone = zone, 
                duration = result["duration"], 
                registration = result["registration"], 
                precept = result["precept"],
                price = result["price"], 
                payment_method= payment_method,
                paid = result["paid"], 
                created_at = result["created_at"],
                brand = result.get("brand"), 
                model = result.get("model"), 
                color = result.get("color") 
            )
            conn.commit()
            cursor.close()
            conn.close()

        except Exception as e:
            return None
        
        return updated_bulletin
        



    
