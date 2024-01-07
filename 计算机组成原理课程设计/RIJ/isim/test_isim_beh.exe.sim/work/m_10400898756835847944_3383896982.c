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

/* This file is designed for use with ISim build 0xfbc00daa */

#define XSI_HIDE_SYMBOL_SPEC true
#include "xsi.h"
#include <memory.h>
#ifdef __GNUC__
#include <stdlib.h>
#else
#include <malloc.h>
#define alloca _alloca
#endif
static const char *ng0 = "/home/ma5hr00m/Downloads/a/pc.v";
static unsigned int ng1[] = {0U, 0U};
static int ng2[] = {4, 0};
static unsigned int ng3[] = {1U, 0U};
static unsigned int ng4[] = {2U, 0U};
static int ng5[] = {2, 0};
static unsigned int ng6[] = {3U, 0U};



static void Initial_16_0(char *t0)
{
    char *t1;
    char *t2;

LAB0:    xsi_set_current_line(17, ng0);
    t1 = ((char*)((ng1)));
    t2 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t2, t1, 0, 0, 32, 0LL);

LAB1:    return;
}

static void Cont_26_1(char *t0)
{
    char t6[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t5;
    char *t7;
    char *t8;
    char *t9;
    char *t10;
    char *t11;
    char *t12;

LAB0:    t1 = (t0 + 3728U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(26, ng0);
    t2 = (t0 + 2568);
    t3 = (t2 + 56U);
    t4 = *((char **)t3);
    t5 = ((char*)((ng2)));
    memset(t6, 0, 8);
    xsi_vlog_unsigned_add(t6, 32, t4, 32, t5, 32);
    t7 = (t0 + 4392);
    t8 = (t7 + 56U);
    t9 = *((char **)t8);
    t10 = (t9 + 56U);
    t11 = *((char **)t10);
    memcpy(t11, t6, 8);
    xsi_driver_vfirst_trans(t7, 0, 31);
    t12 = (t0 + 4296);
    *((int *)t12) = 1;

LAB1:    return;
}

static void Always_28_2(char *t0)
{
    char t14[8];
    char t15[8];
    char *t1;
    char *t2;
    char *t3;
    char *t4;
    char *t5;
    unsigned int t6;
    unsigned int t7;
    unsigned int t8;
    unsigned int t9;
    unsigned int t10;
    char *t11;
    char *t12;
    int t13;
    char *t16;
    unsigned int t17;
    char *t18;

LAB0:    t1 = (t0 + 3976U);
    t2 = *((char **)t1);
    if (t2 == 0)
        goto LAB2;

LAB3:    goto *t2;

LAB2:    xsi_set_current_line(28, ng0);
    t2 = (t0 + 4312);
    *((int *)t2) = 1;
    t3 = (t0 + 4008);
    *((char **)t3) = t2;
    *((char **)t1) = &&LAB4;

LAB1:    return;
LAB4:    xsi_set_current_line(29, ng0);

LAB5:    xsi_set_current_line(30, ng0);
    t4 = (t0 + 1208U);
    t5 = *((char **)t4);
    t4 = (t5 + 4);
    t6 = *((unsigned int *)t4);
    t7 = (~(t6));
    t8 = *((unsigned int *)t5);
    t9 = (t8 & t7);
    t10 = (t9 != 0);
    if (t10 > 0)
        goto LAB6;

LAB7:    xsi_set_current_line(33, ng0);

LAB9:    xsi_set_current_line(34, ng0);
    t2 = (t0 + 1368U);
    t3 = *((char **)t2);

LAB10:    t2 = ((char*)((ng1)));
    t13 = xsi_vlog_unsigned_case_compare(t3, 2, t2, 2);
    if (t13 == 1)
        goto LAB11;

LAB12:    t2 = ((char*)((ng3)));
    t13 = xsi_vlog_unsigned_case_compare(t3, 2, t2, 2);
    if (t13 == 1)
        goto LAB13;

LAB14:    t2 = ((char*)((ng4)));
    t13 = xsi_vlog_unsigned_case_compare(t3, 2, t2, 2);
    if (t13 == 1)
        goto LAB15;

LAB16:    t2 = ((char*)((ng6)));
    t13 = xsi_vlog_unsigned_case_compare(t3, 2, t2, 2);
    if (t13 == 1)
        goto LAB17;

LAB18:
LAB19:
LAB8:    goto LAB2;

LAB6:    xsi_set_current_line(31, ng0);
    t11 = ((char*)((ng1)));
    t12 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t12, t11, 0, 0, 32, 0LL);
    goto LAB8;

LAB11:    xsi_set_current_line(35, ng0);
    t4 = (t0 + 2168U);
    t5 = *((char **)t4);
    t4 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t4, t5, 0, 0, 32, 0LL);
    goto LAB19;

LAB13:    xsi_set_current_line(36, ng0);
    t4 = (t0 + 1528U);
    t5 = *((char **)t4);
    t4 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t4, t5, 0, 0, 32, 0LL);
    goto LAB19;

LAB15:    xsi_set_current_line(37, ng0);
    t4 = (t0 + 2168U);
    t5 = *((char **)t4);
    t4 = (t0 + 1688U);
    t11 = *((char **)t4);
    t4 = ((char*)((ng5)));
    memset(t14, 0, 8);
    xsi_vlog_unsigned_lshift(t14, 32, t11, 32, t4, 32);
    memset(t15, 0, 8);
    xsi_vlog_unsigned_add(t15, 32, t5, 32, t14, 32);
    t12 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t12, t15, 0, 0, 32, 0LL);
    goto LAB19;

LAB17:    xsi_set_current_line(38, ng0);
    t4 = ((char*)((ng1)));
    t5 = (t0 + 1848U);
    t11 = *((char **)t5);
    t5 = (t0 + 2168U);
    t12 = *((char **)t5);
    memset(t15, 0, 8);
    t5 = (t15 + 4);
    t16 = (t12 + 4);
    t6 = *((unsigned int *)t12);
    t7 = (t6 >> 28);
    *((unsigned int *)t15) = t7;
    t8 = *((unsigned int *)t16);
    t9 = (t8 >> 28);
    *((unsigned int *)t5) = t9;
    t10 = *((unsigned int *)t15);
    *((unsigned int *)t15) = (t10 & 15U);
    t17 = *((unsigned int *)t5);
    *((unsigned int *)t5) = (t17 & 15U);
    xsi_vlogtype_concat(t14, 32, 32, 3U, t15, 4, t11, 26, t4, 2);
    t18 = (t0 + 2568);
    xsi_vlogvar_wait_assign_value(t18, t14, 0, 0, 32, 0LL);
    goto LAB19;

}


extern void work_m_10400898756835847944_3383896982_init()
{
	static char *pe[] = {(void *)Initial_16_0,(void *)Cont_26_1,(void *)Always_28_2};
	xsi_register_didat("work_m_10400898756835847944_3383896982", "isim/test_isim_beh.exe.sim/work/m_10400898756835847944_3383896982.didat");
	xsi_register_executes(pe);
}
