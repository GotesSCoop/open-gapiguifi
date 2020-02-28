# Introducció



Inclou scripts per crear nodes a la web de Guifi i extreure'n els paràmetres.

El fitxer env inclou les credencials per a la web de Guifi.net

Comptam amb varis scripts:

* addnode.py: Genera un node a la web de Guifi

* addlink.py: Enllaça un node a la web de Guifi amb un AP

* rmnode.py: Elimina un node de la web de Guifi

* scannode.py: Escaneja un node de la web de Guifi tot cercant els AP més propers 

* printmodels.py: Mostra els id dels models de dispositiu disponibles

## Requisits:
* python3
* pip3 install pyyaml
* pip3 install jinja2

# Scripts

## addnode.py

Crea un node a la web de Guifi.net amb els paràmetres passats. Per loggejar-se a l'API de la web, cal crear un fitxer amb nom env.py que defineixi les variables "username" i "password" amb les credencials corresponents. Retorna l'ID del node creat.

```
Usage: addnode.py -h -t -n node_name -l lat -L lon [-z zone]
Adds node at geographic location identified by lat and lon options. If device_id passed, links this to device_id AP.
    -h, --help      Display help and exit
    -t, --test      Use test.guifi.net instead of production website
    -n, --name      Name of the new node
    -l, --lat       Latitude of the new node (float)
    -L, --lon       Longitude of the new node (float)
    -z, --zone      Zone ID of the new node. Optional. Default 41583 (Sóller)
```

## addlink.py

Afegeix un enllaç client-AP entre el node amb node ID passat i el dispositiu AP passat. Fixau-vos que en cas del node li passam el NODE ID, però en el cas de l'AP li passam el DEVICE_ID.

```
Usage: addlink.py -h -t -n node_id -a ap_id -d device_name [-m MAC]
Links node identified by node_id to device_id AP.
    -h, --help      Display help and exit
    -t, --test      Use test.guifi.net instead of production website
    -n, --node_id       ID of the node to link
    -a, --ap_id     ID of the device of the AP to link to
    -d, --device_name   Name of the device of the node to link from (will be created)
    -m, --mac        MAC of the new device. Optional. Default 00:00:00:00:00:00
```

## rmnode.py

Elimina el node passat i tots els enllaços que hi tenen alguna relació.

```
Usage: rmnode.py -h -t -n node_id
Removes node and all exising links and devices from this node.
    -h, --help      Display help and exit
    -t, --test      Use test.guifi.net instead of production website
    -n, --node_id       ID of the node to remove
```

## scannode.py

Escaneja el node passat i mostra els APs més propers.

```
Usage: scannode.py -h -t -n node_id
Scans AP near the node identified by node_id
    -h, --help      Display help and exit
    -t, --test      Use test.guifi.net instead of production website
    -n, --node NODE_ID  Node to scan nearby APs
```

## getvarfile.py
Treu informació del node node_id i completa la plantilla en jinja2 passada per paràmetre. Es poden afegir, si escau,
valors per l'usuari PPTP i la seva contrasenya.

```
Usage: getvarfile.py -h -t -n node_id -j template_path [ -u pptp_user -p pptp_password ]
Gets the variables of the passed node and renders them in a template. Then, prints the resulting template.
	-h, --help		Display help and exit
	-t, --test		Use test.guifi.net instead of production website
	-n, --node_id		ID of the node
	-j, --template		Jinja2 template to write the variables
	-u, --pptp_user		PPTP username (optional)
	-p, --pptp_password	PPTP user password
```




# Exemples d'ús

## Crea un node a la web de proves i enllaça'l amb un supernode

```
id=$(python3 addnode.py -t -n SOLTest -l 39.780969 -L 2.725782)
python3 addlink.py -t -n $id -a 90379 -d SOLTest-SXT5
```

## Crea un node, consulta els APs propers, i enllaça'l a un d'ells (interactiu)

```
id=$(./addnode.py -n SOLTest -l 39.780969 -L 2.725782)
python3 scannode.py -n $id
python3 addlink.py -n $id -a 66666 -d SOLTest-DISC5 -m ff:bb:dd:dd:aa:aa -i 101
python3 getvarfile.py -n $id -j nodevar_tpl.j2 -u pptpuser -p pptppass > node_"$id"_varfile
```


