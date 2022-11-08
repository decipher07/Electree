const express = require("express");
const monk = require ("monk")
require('dotenv').config();

const app = express();
const url = process.env.MONGODB_URL
const db = monk(url)

app.use(express.json())

async function personDescendant ( name, houseNumber ) {

    var users = db.get('user');

        let newfield = await users.aggregate([
            {
                '$match': {
                  'Name': name,
                  'House Number': houseNumber
                }
            },
            {
                '$graphLookup': {
                    'from': 'user', 
                    'startWith': '$Name', 
                    'connectFromField': 'Name', 
                    'connectToField': 'Relative Name', 
                    'as': 'heirachy'
                }
            }
        ])

        return newfield
}

app.get('/', async (req, res) => {
    
    let { name } = req.body ;
    
    var users = db.get('user');

    var data = await users.aggregate([
        {
          '$match': {
            'Name': name
          }
        }, {
          '$graphLookup': {
            'from': 'user', 
            'startWith': '$Relative Name', 
            'connectFromField': 'Relative Name', 
            'connectToField': 'Name', 
            'as': 'heirachy'
          }
        }
      ])
      
    var response = {
          'self': name
    }
    
    if ( data.length == 0 )
        return res.json(response);
      
    response[data[0].Relation] = data[0]['Relative Name']
      
    for ( person of data[0].heirachy ){
        if ( person['House Number'] == data[0]['House Number']){
            let descendant_data = await personDescendant(person.Name, person['House Number']);
            response[`${data[0]['Relation']}'s ${descendant_data[0].Relation}`] = descendant_data[0]['Relative Name']

            var descendant_data_hierachy = descendant_data[0]['heirachy'];
            
            for ( person of descendant_data_hierachy ){
                if ( person.Name == name )
                    continue ;

                if ( person.Relation == 'father' ){
                    if ( person.Gender == "FEMALE" )
                        response[`${data[0]['Relation']}'s daughter`] = person.Name
                    else
                        response[`${data[0]['Relation']}'s son`] = person.Name
                            
                }
            }

        }
        
        
    }

    res.json(response);
})

const port = process.env.PORT
app.listen(port, () => console.log(`Server running at Port ${port}`));