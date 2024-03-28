from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:

    # Dictionary of objects saved to the database.
    all = {}

    def __init__(self, year, summary, employee_id, id=None):
        self.id = id
        self._year = year
        self._summary = summary
        self._employee_id = employee_id

    def __repr__(self):
        return (
            f"<Review {self.id}: {self._year}, {self._summary}, "
            + f"Employee: {self._employee_id}>"
        )
    
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self,year):
        if isinstance(year,int) and year>=2000:
            self._year=year
        else:raise ValueError("Year must be an integer of valu greater than 2000")
   
    @property
    def summary(self):
        return self._summary
    
    @summary.setter
    def summary(self,summary):
        if isinstance(summary,str) and len(summary)>0:
            self._summary=summary
        else:raise ValueError("Summary must be an integer of length greater 0")
    
    @property
    def employee_id(self):
        return self._employee_id
    
    @employee_id.setter
    def employee_id(self,employee_id):
        if Employee.find_by_id(employee_id) :
            self._employee_id=employee_id
        else:raise ValueError("Employee_id must be must be an instance that has been persisted to the employees table ")
    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Review instances """
        sql = """
            CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY,
            year INT,
            summary TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Review  instances """
        sql = """
            DROP TABLE IF EXISTS reviews;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the year, summary, and employee id values of the current Review object.
        Update object id attribute using the primary key value of new row.
        Save the object in local dictionary using table row's PK as dictionary key"""
        CURSOR.execute("INSERT INTO reviews(year,summary,employee_id) VALUES(?,?,?)",(self._year,self._summary,self._employee_id))
        CONN.commit()

        self.id=CURSOR.lastrowid
        type(self).all[self.id]=self
    @classmethod
    def create(cls, year, summary, employee_id):
        """ Initialize a new Review instance and save the object to the database. Return the new instance. """
        new_review=cls(year,summary,employee_id)
        new_review.save()
        return new_review 
   
    @classmethod
    def instance_from_db(cls, row):
        """Return an Review instance having the attribute values from the table row."""
        # Check the dictionary for  existing instance using the row's primary key
        new_review=cls.all.get(row[0])
        if new_review:
            new_review.year=row[1]
            new_review.summary=row[2]
            new_review.employee_id=row[3]
        else:
            new_review=cls(row[1],row[2],row[3])
            new_review.id=row[1]
        return new_review

    @classmethod
    def find_by_id(cls, id):
        """Return a Review instance having the attribute values from the table row."""
        sql="SELECT * FROM reviews WHERE id=?"
        rows=CURSOR.execute(sql,(id,)).fetchone()
        return cls.instance_from_db(rows) if rows else None

    def update(self):
        """Update the table row corresponding to the current Review instance."""
        sql="UPDATE reviews SET year=?, summary=?, employee_id=? WHERE id=? "
        CURSOR.execute(sql,(self._year,self._summary,self._employee_id,self.id))
        
    def delete(self):
        """Delete the table row corresponding to the current Review instance,
        delete the dictionary entry, and reassign id attribute"""
        sql="DELETE  FROM reviews WHERE id=?"
        CURSOR.execute(sql,(self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id=None

    @classmethod
    def get_all(cls):
        """Return a list containing one Review instance per table row"""
        sql="SELECT * FROM reviews"
        rows=CURSOR.execute(sql).fetchall()
        CONN.commit()
        return [cls.instance_from_db(row)for row in rows]
        

