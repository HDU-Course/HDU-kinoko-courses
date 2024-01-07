/**********************************************************************/
/*   ____  ____                                                       */
/*  /   /\/   /                                                       */
/* /___/  \  /                                                        */
/* \   \   \/                                                       */
/*  \   \        Copyright (c) 2003-2009 Xilinx, Inc.                */
/*  /   /          All Right Reserved.                                 */
/* /---/   /\                                                         */
/* \   \  /  \                                                      */
/*  \___\/\___\                                                    */
/***********************************************************************/

#include "xsi.h"

struct XSI_INFO xsi_info;



int main(int argc, char **argv)
{
    xsi_init_design(argc, argv);
    xsi_register_info(&xsi_info);

    xsi_register_min_prec_unit(-12);
    xilinxcorelib_ver_m_04284627112054182733_1420689212_init();
    xilinxcorelib_ver_m_18166792875774041790_1862936372_init();
    xilinxcorelib_ver_m_17738287534884592592_0050634287_init();
    xilinxcorelib_ver_m_10066368518302646626_2552104820_init();
    work_m_05240187959938530918_1015039846_init();
    work_m_10400898756835847944_3383896982_init();
    work_m_08814850090432149931_1282137562_init();
    work_m_14508931181450511290_2749254585_init();
    work_m_07574449322237014137_0886308060_init();
    xilinxcorelib_ver_m_01834407678936685707_3805459806_init();
    xilinxcorelib_ver_m_10066368518302646626_0557065841_init();
    work_m_14056882636803624207_1948799799_init();
    work_m_13890797829769461489_3036013123_init();
    work_m_16541823861846354283_2073120511_init();


    xsi_register_tops("work_m_13890797829769461489_3036013123");
    xsi_register_tops("work_m_16541823861846354283_2073120511");


    return xsi_run_simulation(argc, argv);

}
