/**
  Generated Main Source File

  Company:
    Microchip Technology Inc.

  File Name:
    main.c

  Summary:
    This is the main file generated using PIC10 / PIC12 / PIC16 / PIC18 MCUs

  Description:
    This header file provides implementations for driver APIs for all modules selected in the GUI.
    Generation Information :
        Product Revision  :  PIC10 / PIC12 / PIC16 / PIC18 MCUs - 1.81.7
        Device            :  PIC18F46K22
        Driver Version    :  2.00
 */

/*
    (c) 2018 Microchip Technology Inc. and its subsidiaries. 
    
    Subject to your compliance with these terms, you may use Microchip software and any 
    derivatives exclusively with Microchip products. It is your responsibility to comply with third party 
    license terms applicable to your use of third party software (including open source software) that 
    may accompany Microchip software.
    
    THIS SOFTWARE IS SUPPLIED BY MICROCHIP "AS IS". NO WARRANTIES, WHETHER 
    EXPRESS, IMPLIED OR STATUTORY, APPLY TO THIS SOFTWARE, INCLUDING ANY 
    IMPLIED WARRANTIES OF NON-INFRINGEMENT, MERCHANTABILITY, AND FITNESS 
    FOR A PARTICULAR PURPOSE.
    
    IN NO EVENT WILL MICROCHIP BE LIABLE FOR ANY INDIRECT, SPECIAL, PUNITIVE, 
    INCIDENTAL OR CONSEQUENTIAL LOSS, DAMAGE, COST OR EXPENSE OF ANY KIND 
    WHATSOEVER RELATED TO THE SOFTWARE, HOWEVER CAUSED, EVEN IF MICROCHIP 
    HAS BEEN ADVISED OF THE POSSIBILITY OR THE DAMAGES ARE FORESEEABLE. TO 
    THE FULLEST EXTENT ALLOWED BY LAW, MICROCHIP'S TOTAL LIABILITY ON ALL 
    CLAIMS IN ANY WAY RELATED TO THIS SOFTWARE WILL NOT EXCEED THE AMOUNT 
    OF FEES, IF ANY, THAT YOU HAVE PAID DIRECTLY TO MICROCHIP FOR THIS 
    SOFTWARE.
 */

#include "mcc_generated_files/mcc.h"
#include "nrf24_lib.h"
#include <string.h>

NRF24_INIT_STATUS ret;
unsigned char i;
char buffer1[20];
unsigned char bufferTX[32];
unsigned char bufferRX[32];

#define NRF24L01_TX_EX  1
#define NRF24L01_RX_EX  !NRF24L01_TX_EX

void blink_led() {
    LED_Toggle();
}

/*
                         Main application
 */
void main(void) {
    // Initialize the device
    SYSTEM_Initialize();

    // If using interrupts in PIC18 High/Low Priority Mode you need to enable the Global High and Low Interrupts
    // If using interrupts in PIC Mid-Range Compatibility Mode you need to enable the Global and Peripheral Interrupts
    // Use the following macros to:

    // Enable the Global Interrupts
    INTERRUPT_GlobalInterruptEnable();

    // Disable the Global Interrupts
    //INTERRUPT_GlobalInterruptDisable();

    // Enable the Peripheral Interrupts
    INTERRUPT_PeripheralInterruptEnable();

    // Disable the Peripheral Interrupts
    //INTERRUPT_PeripheralInterruptDisable();

    TMR0_SetInterruptHandler(blink_led);

    printf("Timer0 init Done\r\n");

    SPI1_Open(SPI1_DEFAULT);
#if NRF24L01_TX_EX
    ret = nrf24_rf_init(TX_MODE, 115); // Tx mode with 2400+115 Ghz RF frq
#elif NRF24L01_RX_EX
    ret = nrf24_rf_init(RX_MODE, 115); // Rx mode with 2400+115 Ghz RF frq
#endif

    if (ret == NRF24_INIT_OK) {

        printf("###############################################################\r\n");
        printf("NRF24L01 Initialize successful\r\n");
        nrf24_printf_rf_config();
        printf("###############################################################\r\n");

        while (1) {
#if NRF24L01_TX_EX
            static char val = 0;
            sprintf((char*)bufferTX, "Hello Arduino %d", val);
            printf("NRF24 Send Data: %s\r\n", bufferTX);
            nrf24_send_rf_data(bufferTX);
            val++;
            __delay_ms(100);
#elif NRF24L01_RX_EX
            while (nrf24_is_rf_data_available()) {
            }
            nrf24_read_rf_data(bufferRX);
            printf("NRF24 Receive Data: %s\r\n", bufferRX);
            __delay_ms(10);
#endif
            __delay_ms(100);
        }
    } else {
        printf("###############################################################\r\n");
        printf("Failed Initialize NRF24L01\r\n");
        printf("###############################################################\r\n");
        while (1) {

        }
    }
}
/* ------------------------------------------------------------------------- */

/**
 End of File
 */