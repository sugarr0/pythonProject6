from requests import get, post, delete

print(post("http://127.0.0.1:5000/api/users", json={'email': 's',
                                                    'password': 'd',
                                                    'name': 'df',
                                                    'surname': 'dfg',
                                                    'city': 'd',
                                                    }).json())
