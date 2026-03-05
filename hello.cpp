#include <iostream>
#include <cmath>


int main(){
    int capacity;
    int cars;
    int choice;

    std::cout<<"1.Parking lot capacity\n";
    std::cout<<"2.Car enter\n";
    std::cout<<"3.Car Exit";
    std::cout<<"4.Parking lot Status\n";
    std::cout<<"5.Enter your choice:";
    std::cin>>choice;

    switch (choice)
    {
    case 1:
    std::cout<<"can hold 5 cars";
    break;
     case 2:
    std::cout<<"car parked successfully";
    break;
     case 3:
    std::cout<<"car leaves parking";
    break;
     case 4:
    std::cout<<"4 slots available";
    break;

   
        
    
    default:
    std::cout<<"invalid input";
        break;
    }


  
  
 
return 0;
}
