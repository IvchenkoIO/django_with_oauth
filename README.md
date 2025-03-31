for deployment:
  in case it gives errors , try to delete all of the images/containers and build again (docker-compose up --build)


for oauth: 
  login : test_u1
  password : rootroot


AUTH_SERV:
  /admin - admin page of oauth serv (applications etc)
RESOURCE_SERV:
  /api/photos - the url that returns data
CLIENT_SERV:
  /login - to start the oauth process and retreive data from RESOURCE_SERV
