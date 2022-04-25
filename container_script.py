import docker
client = docker.from_env()
#image = client.images.pull("wordpress")
import logging

log_file = 'container_log.log'
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler = logging.FileHandler(log_file)
handler.setFormatter(formatter)
logger = logging.getLogger('container_log')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

IMAGES = {"5.6.8": {"7.4": "wordpress_custom5.6.8:7.4", "8.1": "wordpress_custom5.6.8:8.1"},
          "latest": {"7.4": "wordpress_custom_latest:7.4", "8.1": "wordpress_custom_latest:8.1"}
        }

def create_container(DB_NAME, DB_USER, DB_PASSWORD, wp_version, php_version):

    try:
        logger.info("making container")
        container = client.containers.run(IMAGES[wp_version][php_version],
                environment= ["WORDPRESS_DB_HOST=206.189.138.203", "WORDPRESS_DB_USER={}".format(DB_USER),
                "WORDPRESS_DB_PASSWORD={}".format(DB_PASSWORD), "WORDPRESS_DB_NAME={}".format(DB_NAME),
                "VIRTUAL_HOST=206.189.138.203", "VIRTUAL_PATH=^~/{}".format(DB_NAME)],
                name = DB_NAME, network = 'nginx-proxy', detach = True)

    except docker.errors.ContainerError as error:
        logger.error(error)
        return 500
    except docker.errors.APIError as error:
        logger.error(error)
        return 500

    logger.info("Created Container: "+ str(client.containers.get(DB_NAME)))
    return 200

def delete_container(name):
    try:
        logger.info("deleting container.. ")
        container = client.containers.get(name)
        container.stop()
        container.remove()
    except docker.errors.APIError as error:
        logger.error(error)
        return 500
    logger.info("Deleted container: "+name)
    return 200

