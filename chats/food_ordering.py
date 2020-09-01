from jumpscale.loader import j
from jumpscale.sals.chatflows.chatflows import GedisChatBot, chatflow_step


class FoodChat(GedisChatBot):
    # Sample data
    menus = {
        "3 Burger": {"main": ["Cheese Burger", "Douple Burger"], "sides": ["fries", "Onion rings"]},
        "3 Pizza": {"main": ["Chicken Pizza", "Beef Pizza", "Cheese Pizza"], "sides": ["fries", "Cheese"]},
    }

    # Chatflow steps
    steps = ["client_name_select", "restaurant_select", "restaurant_main_dish", "restaurant_side_dish", "confirmation"]

    # Chatflow title
    title = "Food ordering Chat"

    @chatflow_step("Name")
    def client_name_select(self):
        # Ask the user about his name
        self.client_name = self.string_ask("Hello, What's your name?", required=True)

    @chatflow_step("Restaurant")
    def restaurant_select(self):
        # display a dropdown containing your favourite Restaurants
        self.restaurant_name = self.drop_down_choice("Please select a Resturant", list(self.menus.keys()))

    @chatflow_step("Main Dish")
    def restaurant_main_dish(self):
        # display the main dishes of the selected restaurant so the user can choose only one dish
        self.main_dish = self.single_choice("Please Select your main dish", self.menus[self.restaurant_name]["main"])

        # ask about the mount (this accepts any integer)
        self.amount = self.int_ask("How many {} do you want".format(self.main_dish), min=2, max=3)

    @chatflow_step("Side Dish")
    def restaurant_side_dish(self):
        # ask about the side dishes (the user can choose multible side dishes)
        self.side_dish = self.multi_choice(
            "what do you want with your order", self.menus[self.restaurant_name]["sides"]
        )

    @chatflow_step(title="Confirmation", disable_previous=True, final_step=True)
    def confirmation(self):
        # Now you can add any logic you want here to send the order to the restaurant
        # Then we can show a report to the user about his order using md format
        report = f"""# Hello {self.client_name}
## Your order has been confirmed \n\n<br>\n
### You have ordered : {self.amount} {self.main_dish} with {self.side_dish}
        """

        self.md_show(report, md=True)


chat = FoodChat
