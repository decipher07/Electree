const express = require("express");
const monk = require ("monk")

const app = express();
const url = 'mongodb://localhost:27017/elecvotes'
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
    
    // var data = await users.find({ $or : [ { "Name" : name } , { "Relative Name" : name } ] });
    // console.log(typeof(data));
    // console.log(data.length)

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

app.listen(3000, () => console.log('Server running at Port 3000'));