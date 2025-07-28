from setuptools import setup, find_packages

setup(
    name="map_skin_project",               # 套件名稱（可以自訂）
    version="0.1",                         # 初始版本號
    description="Styled static map generator using OSM and Python",  # 描述
    packages=find_packages(where="src"),  # 自動找 src/ 裡所有模組
    package_dir={"": "src"},              # 告訴 pip 原始碼在哪
    install_requires=[                    # 安裝這些依賴
        "osmnx",
        "geopandas",
        "matplotlib",
        "shapely"
    ],
)
