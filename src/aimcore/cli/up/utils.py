import os
import sys

from aim._sdk.configs import AIM_ENV_MODE_KEY


def build_db_upgrade_command():
    from aimcore import web
    web_dir = os.path.dirname(web.__file__)
    migrations_dir = os.path.join(web_dir, 'migrations')
    if os.getenv(AIM_ENV_MODE_KEY, 'prod') == 'prod':
        ini_file = os.path.join(migrations_dir, 'alembic.ini')
    else:
        ini_file = os.path.join(migrations_dir, 'alembic_dev.ini')
    return [sys.executable, '-m', 'alembic', '-c', ini_file, 'upgrade', 'head']


def build_uvicorn_command(host, port, num_workers, uds_path, ssl_keyfile, ssl_certfile, log_level, pkg_name):
    cmd = [sys.executable, '-m', 'uvicorn',
           '--host', host, '--port', f'{port}',
           '--workers', f'{num_workers}']
    if os.getenv(AIM_ENV_MODE_KEY, 'prod') == 'prod':
        log_level = log_level or 'error'
    else:
        import aim
        import aimstack
        from aimcore import web as aim_web

        cmd += ['--reload']
        cmd += ['--reload-dir', os.path.dirname(aim.__file__)]
        cmd += ['--reload-dir', os.path.dirname(aim_web.__file__)]
        cmd += ['--reload-dir', os.path.dirname(aimstack.__file__)]

        from aim._sdk.package_utils import Package
        if pkg_name not in Package.pool:
            Package.load_package(pkg_name)
            pkg = Package.pool[pkg_name]
            cmd += ['--reload-dir', os.path.dirname(pkg._path)]

        log_level = log_level or 'debug'
    if uds_path:
        cmd += ['--uds', uds_path]
    if ssl_keyfile:
        cmd += ['--ssl-keyfile', ssl_keyfile]
    if ssl_certfile:
        cmd += ['--ssl-certfile', ssl_certfile]
    cmd += ['--log-level', log_level.lower()]
    cmd += ['aimcore.web.run:app']
    return cmd


def get_free_port_num():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    port_num = s.getsockname()[1]
    s.close()
    return port_num
