from app import app


## first positive test case for '/hello' route
def test_hello_route_success():
    tester = app.test_client()
    response = tester.get('/hello')

    assert response.status_code==200


# def test_hello_route_failure():
#     tester = app.test_client()
#     response = tester.get('/hello')

#     assert response.status_code==500



## positive test case for '/predict' route

def test_predict_route_success():
    tester = app.test_client()

    data = {"gestation":[279],
            "parity":[0],
            "age":[27],
            "height":[70],
            "weight":[100],
            "smoke":[0]
            }
    response = tester.post("/predict", json=data)

    assert response.status_code==200




def test_predict_route_invalid_data():
    tester = app.test_client()

    data = {"gestation":['279'],
            "parity":[0],
            "age":[27],
            "height":[70],
            "weight":[100],
            "smoke":[0]
            }
    response = tester.post("/predict", json={})

    assert response.status_code==400



def test_predict_route_wrong_url():
    tester = app.test_client()

    data = {"gestation":[279],
            "parity":[0],
            "age":[27],
            "height":[70],
            "weight":[100],
            "smoke":[0]
            }
    response = tester.post("/oredict", json=data)

    assert response.status_code==404


def test_predict_route_wrong_method():
    tester = app.test_client()

    data = {"gestation":[279],
            "parity":[0],
            "age":[27],
            "height":[70],
            "weight":[100],
            "smoke":[0]
            }
    response = tester.get("/predict", json=data)

    assert response.status_code==405