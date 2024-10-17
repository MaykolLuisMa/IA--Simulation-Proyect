#dependencias
from src.code.company import Factory
from src.code.product import Product, ProductMount

#apartado de tecnologia
######################################################################################################################
#celular
pantalla = Product('pantalla', 'tecnology', 5, [])
placa_cel = Product('placa_cel', 'tecnology', 40, [])
lente = Product('lente', 'tecnology', 3, [])
req_celular = [ProductMount(pantalla, 1), ProductMount(placa_cel, 1), ProductMount(lente, 3)]
celular = Product('celular', 'tecnology', 100, req_celular)

#computadora
mouse = Product('mouse', 'tecnology', 1, [])
placa_pc = Product('placa_pc', 'tecnology', 80, [])
tarjeta_video = Product('tarjeta de video', 'tecnology', 40, [])
teclado = Product('teclado', 'tecnology', 4, [])
req_pc = [ProductMount(mouse, 1), ProductMount(placa_pc, 1), ProductMount(tarjeta_video, 2), ProductMount(teclado, 1)]
pc = Product('pc', 'tecnology', 450, req_pc)

#factoria del apartado de tecnologia
tec_factory = Factory('tecnology')

#productos de tecnologia
tec_celular = [ProductMount(pantalla, 10000), ProductMount(placa_cel, 6000), ProductMount(lente, 12000), ProductMount(celular, 3000)]
tec_computadora = [ProductMount(mouse, 10000), ProductMount(placa_pc, 3000), ProductMount(tarjeta_video, 5000), ProductMount(teclado, 8500), ProductMount(pc, 1750)]
tec_products = tec_celular + tec_computadora
######################################################################################################################

#apartado de transporte
"""car = Product('car', 'transport', 40000)
bike = Product('bike', 'transport', 2000)
truck = Product('truck', 'transport', 60000)
raw_car = RawMaterial('raw car', car, 1200)
raw_bike = RawMaterial('raw bike', bike, 200)
raw_truck = RawMaterial('raw truck', truck, 2000)
factory_car = Factory(raw_car)
factory_bike = Factory(raw_bike)
factory_truck = Factory(raw_truck)
transport_raw = [RawMaterialMount(raw_car, 1000), RawMaterialMount(raw_bike, 2000), RawMaterialMount(raw_truck, 500)]
transport_factory = [factory_car, factory_bike, factory_truck]"""

