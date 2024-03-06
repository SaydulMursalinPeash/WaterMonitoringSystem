import flet as ft
from flet import *
import requests
import json
import asyncio
import websockets

def get_sensor_data():
    url = 'http://192.168.254.106:8000/api/sensors/'
    response = requests.get(url)
    if response.status_code == 200:  
        data = response.json()
        print(data)
        return data['data']
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
get_sensor_data()
def _expand_sensor(e):
    if(e.data=='true'):
        pass
    else:
        pass


async def main(page:Page):
    page.bgcolor=ft.colors.GREY_800
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER
    page.vertical_alignment=ft.MainAxisAlignment.CENTER
    text_inp=TextField(label='Sensor name',border_color='white',color='white',border_radius=15,text_size=15)
    temp=Text(f"Temperature: 0",size=18,color=ft.colors.WHITE54,weight='w400')
    tds=Text(f"TDS: 0",size=18,color=ft.colors.WHITE54,weight='w400')
    do=Text(f"DO: 0",size=18,color=ft.colors.WHITE54,weight='w400')
    cond=Text(f"Condactivity: 0",size=18,color=ft.colors.WHITE54,weight='w400')
    sensor_name=Text('Name',size=20,weight='w500',color='white')
    
    async def small(e):
        if e=="false":
            main_container.content.controls[0].controls[0].height=640*0.4
            await main_container.content.controls[0].update_async()
        else:
            main_container.content.controls[0].controls[0].height=640
            await main_container.content.controls[0].update_async()
    #top container
    data_container=Container(
        width=300,
        padding=10,
        height=660*0.4,
        visible=False,
        gradient=LinearGradient(
            begin=alignment.bottom_left,
            end=alignment.top_right,
            colors=['#212130','#39304A']
        ),
        animate=animation.Animation(
                duration=350,
                curve='decelerate',
                
            ),
        border_radius=35,
        content=Column(
            alignment='start',
            controls=[
                Row(
                  alignment='center',
                  controls=[
                      sensor_name
                  ]  
                ),
                Divider(height=8,thickness=1,color='white10'),
                temp,
                tds,
                do,
                cond,
                
            ]
        )
    )
    soc=0
    async def search_sensor(e):
        
        s_name=text_inp.value
        sensor_name.value=f"{s_name}"
        if s_name=='':
            data_container.visible=False
            await small(e='true')
            await page.update_async()
            return
        await small(e='false')
        data_container.visible=True
        await page.update_async()
        #print(name)
        try:
            con=await websockets.connect("ws://192.168.254.106:8000/ws/sensor/"+s_name+"/")
        except:
            sensor_name.value="Connection failed!!"
            await page.update_async()
            
            
        
        while True:
            #print('trying')
            try:
                if(s_name!=text_inp.value):
                    break
                #print(f'wss://waterserver-vsqt.onrender.com/ws/sensor/{text_inp.value}/')
                data1 = await con.recv()
                data=json.loads(data1)
                temp.value=f"Temperature: {round(float(data['temp'])-5,2)} ^C"
                tds.value=f"TDS: {round(float(data['tds']),2)} ppm" if float(data['tds'])>30 else 'TDS: Not in water!!'
                do.value=f"DO: {round(float(data['do']),2)} ppm " if float(data['tds'])>30 else 'DO: Not in water!!'
                cond.value=f"Conductivity: {round(float(data['cond']),2)} \u00B5S/cm" if float(data['tds'])>30 else 'Conductivity: Not in water!!'
                    
                    
                await page.update_async()
            except websockets.exceptions.ConnectionClosedError:
                print("Connection closed")
                break
        
               
    async def _top():
        top=ft.Container(
            width=300,
            height=640,
            gradient=LinearGradient(
                begin=alignment.bottom_left,
                end=alignment.top_right,
                colors=['lightblue600','lightblue900']
            ),
            border_radius=35,
            animate=animation.Animation(
                duration=350,
                curve='decelerate',
                
            ),
            
            padding=10,
            content=Column(
                alignment='start',
                spacing=10,
                controls=[
                    Row(
                        alignment='center',
                        controls=[
                            Text(
                                'WatMon',
                                size=20,
                                weight='w700',
                                color='white'
                                
                            )
                        ]
                    ),
                    Container(
                        padding=padding.only(bottom=5)
                    ),
                    Row(
                        alignment='center',
                        spacing=15,
                        controls=[
                            Column(
                                controls=[
                                    Container(
                                    height=90,
                                    width=90,
                                    image_src='Water/assets/wd4.png',
                                    bgcolor='white',
                                    border_radius=75
                                
                                    )
                                ]
                            ),
                            Column(
                                spacing=5,
                                horizontal_alignment='center',
                                
                                controls=[
                                    Text(
                                        "An smart realtime sensor based filtered water monitoring system.",
                                        width=150,
                                        size=15,
                                        color='white',
                                        weight='w500'
                                        

                                    )
                                ],
                                
                            )
                        ]
                    ),
                    Divider(height=8,thickness=1,color='white10'),
                    Row(
                        alignment='center',
                        controls=[
                            Container(
                                height=35,
                                width=200,
                                content=text_inp,
                                
                            ),
                            IconButton(icons.SEARCH,bgcolor=ft.colors.WHITE30,on_click=search_sensor)
                        ]
                    )
                ]
            )
        )
        return top
    main_container=Container(
        width=310,
        height=660,
        border_radius=35,
        bgcolor='black',
        padding=10,
        content=Stack(
            width=300,
            height=550,
            controls=[
                Column(
                    alignment='start',
                    controls=[
                        await _top(),
                        data_container
                        
                    ]
                )
            ]
        )
    )
    await page.add_async(main_container)
    

ft.app(main,assets_dir='assets')

    