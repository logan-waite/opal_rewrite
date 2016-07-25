# OPAL

OPAL is a system centered around the client. Clients can buy various products (normally services), and the user can keep track of these clients, the products they have bought, and any appointments they have with these clients.

### Clients

Clients are the backbone of the system, and are served from the "clients" folder. Each client should have the following information:

 - Name
 - Email(s)
 - Phone number(s)
 - Address (right now we don't care if it's mailing or street, so we don't specify)
 - Links to past products/services that the client has had, in addition to any present and future.

The current database model for clients, as determined by Django's ORM, is as follows:

**Client:**
- first_name : First name of the client (also includes middle name(s) if applicable)
- last_name : Last name of the client (Literally pulls the last word from the full_name string)
- street_address
- city
- state
- zipcode
- events : a [ManyToManyField](https://docs.djangoproject.com/en/1.9/topics/db/models/#many-to-many-relationships) that links to the Event object.
        
**Email:**
- client : a [ForeignKey](https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey) that links to the client
- email : an email for the client
        
**Phone:**
- client : a [ForeignKey](https://docs.djangoproject.com/en/1.9/ref/models/fields/#django.db.models.ForeignKey) that links to the Client
- phone : an phone number for the client

### Events
Events are major gatherings that multiple people are a part of. Every event should have the following:
- A name
- A start date/time
- An end date/time
- Where the event is taking place
- A checklist of items needed for the event to happen successfully
    
The current database model for events, as determined by Django's ORM, is as follows:

**Event**
- name : The name of the event (for marketing, telling them apart, whatever.)
- description : What the event is about.
- start : The date and time the event starts ( a [DateTimeField](https://docs.djangoproject.com/en/1.9/ref/models/fields/#datetimefield) )
- end : The date and time the event ends ( a [DateTimeField](https://docs.djangoproject.com/en/1.9/ref/models/fields/#datetimefield) )
- 
### Services

### Products
