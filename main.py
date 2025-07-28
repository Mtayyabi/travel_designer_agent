import os

from agents import Agent, Runner, OpenAIChatCompletionsModel, function_tool
import dotenv
from openai import AsyncOpenAI, base_url
from dotenv import find_dotenv, load_dotenv
import chainlit as cl

load_dotenv(find_dotenv())

#load enviorment variables
gemini_api_key = os.getenv("GEMINI_API_KEY")
base_url = os.getenv("BASE_URL")

#setup model configuration
@cl.on_chat_start
async def start():
    #external client
    client = AsyncOpenAI(
        api_key=gemini_api_key,
        base_url=base_url
    )
    #model
    model = OpenAIChatCompletionsModel(
        model="gemini-2.5-flash",
        openai_client=client
    )

    #tools
    @function_tool
    async def get_flights(flight_options):
        """ 
        when user ask for book flight you return the flight info
        """
        flight_options = [
        {
            "flightNumber": "AA123",
            "airline": "American Airlines",
            "departureAirport": "JFK",
            "arrivalAirport": "LAX",
            "departureTime": "2025-07-28T08:00:00Z",
            "arrivalTime": "2025-07-28T11:30:00Z",
            "duration": "5h 30m",
            "status": "On Time",
            "price": 299.99,
            "seatsAvailable": 45
        },
        {
            "flightNumber": "DL456",
            "airline": "Delta Air Lines",
            "departureAirport": "KHI",
            "arrivalAirport": "MIA",
            "departureTime": "2025-07-28T10:15:00Z",
            "arrivalTime": "2025-07-28T12:45:00Z",
            "duration": "5h 30m",
            "status": "Delayed",
            "price": 275.50,
            "seatsAvailable": 22
        },
        {
            "flightNumber": "UA789",
            "airline": "United Airlines",
            "departureAirport": "ORD",
            "arrivalAirport": "MIA",
            "departureTime": "2025-07-28T14:00:00Z",
            "arrivalTime": "2025-07-28T17:10:00Z",
            "duration": "3h 10m",
            "status": "On Time",
            "price": 189.00,
            "seatsAvailable": 60
        },
        {
            "flightNumber": "SW101",
            "airline": "Southwest Airlines",
            "departureAirport": "DEN",
            "arrivalAirport": "PHX",
            "departureTime": "2025-07-28T09:30:00Z",
            "arrivalTime": "2025-07-28T11:15:00Z",
            "duration": "1h 45m",
            "status": "Boarding",
            "price": 129.99,
            "seatsAvailable": 15
        },
           {
            "flightNumber": "SQ201",
            "airline": "London Airlines",
            "departureAirport": "LON",
            "arrivalAirport": "MLE",
            "departureTime": "2025-07-28T09:30:00Z",
            "arrivalTime": "2025-07-28T11:15:00Z",
            "duration": "1h 45m",
            "status": "Boarding",
            "price": 129.99,
            "seatsAvailable": 15
        }
    ]
        return flight_options


    #tool for suggest hotels
    @function_tool
    async def suggest_hotels(suggest_hotel):
        """ 
        when user ask for hotels you suggest them the hotels
        """

        suggest_hotel = [
            
        {
            "city": "Los Angeles",
            "hotelId": "H001",
            "name": "Hilton Los Angeles Downtown",
            "rating": 4.4,
            "pricePerNight": 159.99,
            "amenities": ["Free Wi-Fi", "Pool", "Gym", "Restaurant"],
            "address": "929 S Broadway, Los Angeles, CA 90015",
            "checkInTime": "15:00",
            "checkOutTime": "12:00",
            "availability": 25
        },
        {
            "city": "San Francisco",
            "hotelId": "H002",
            "name": "Marriott Marquis San Francisco",
            "rating": 4.5,
            "pricePerNight": 199.00,
            "amenities": ["Free Wi-Fi", "Spa", "Business Center", "Bar"],
            "address": "780 Mission St, San Francisco, CA 94103",
            "checkInTime": "16:00",
            "checkOutTime": "11:00",
            "availability": 18
        },
        {
            "city": "Miami",
            "hotelId": "H003",
            "name": "InterContinental Miami",
            "rating": 4.3,
            "pricePerNight": 179.99,
            "amenities": ["Waterfront Views", "Pool", "Fitness Center", "Free Wi-Fi"],
            "address": "100 Chopin Plaza, Miami, FL 33131",
            "checkInTime": "15:00",
            "checkOutTime": "12:00",
            "availability": 30
        },
        {
            "city": "Phoenix",
            "hotelId": "H004",
            "name": "Hyatt Regency Phoenix",
            "rating": 4.2,
            "pricePerNight": 139.50,
            "amenities": ["Pool", "Restaurant", "Free Wi-Fi", "Pet-Friendly"],
            "address": "122 N 2nd St, Phoenix, AZ 85004",
            "checkInTime": "15:00",
            "checkOutTime": "11:30",
            "availability": 12
        },
        {
            "city": "New York",
            "hotelId": "H005",
            "name": "The Plaza Hotel",
            "rating": 4.7,
            "pricePerNight": 349.99,
            "amenities": ["Spa", "Free Wi-Fi", "Luxury Dining", "Concierge"],
            "address": "768 5th Ave, New York, NY 10019",
            "checkInTime": "15:00",
            "checkOutTime": "12:00",
            "availability": 8
        }

            
    
        ]
        return suggest_hotel
    




    #Agent 1
    destination_agent = Agent(
        name= "Destination Assistant",
        instructions= """
        You are a helpful assistant for find destinations and places for travel, picnic, holidays, vacation etc.

        when user ask for destination and places you suggest them the  destination with or without based on their moods and intrest .

        do not answer anything else
        """,
        model = model
    )
    #Agent 2
    booking_agent = Agent(
        name= "Travel Booking",
        instructions= """ 
        You are travel booking agent you simulate travel bookings.
        when user ask for flights you call 'get_flights' tool,
        when user ask for hotels you call 'suggest_hotels' tool

        do not answer anything
        """,
        model = model,
        tools=[get_flights, suggest_hotels]
    )
    #Agent 3
    explore_agent = Agent(
        name= "Explore",
        instructions= """
        you are a expolre assistant, when user ask for attraction and food you tell them according to the country, city and places.
        suggest their famous foods, restuarants
        do not answer anything else
        
        """,
        model = model
    )

    #Triage agent
    triage_agent = Agent(
        name= "Triage Agent",
        instructions= """ 
        You determine which agent should handle the user's request based on the nature of the inquiry.
        if user ask for place suggestion and anything related to travel you hand off the task to the 'destination_agent',
        if user ask for food and attractions you hand off the task to the 'explore_agent'
        when user ask for booking you handoff the task to the 'booking_agent'
        do not answer anything un related quiry.
        if quiry is unrelated politely decline and tell them you are a 'Travel agent'

        """,
        model = model,
        handoffs= [destination_agent, explore_agent, booking_agent]
    )

    #now we set user sessions variables'
    cl.user_session.set("main_agent", triage_agent)
    cl.user_session.set("chat_history", [])

    #welcome message
    await cl.Message(content="Welcome to the AI Travel Designer Agent, how can I help you?").send()


#now we setup our on_meesage
@cl.on_message
async def main(message: cl.Message):

    #dummy message untill our actual reponse
    msg = cl.Message(content="Thinking...")
    await msg.send()


    #now we get our user session
    main_agent = cl.user_session.get("main_agent")
    history = cl.user_session.get("chat_history")

    #append history in main func para
    history.append({"role": "user", "content": message.content})

    #runner
    result = Runner.run_sync(
        main_agent,
        input = history
    )
    response_content = result.final_output

    #update dummy msg with actual reponse
    msg.content = response_content
    await msg.send()

    #update history
    cl.user_session.set("chat_history", result.to_input_list())