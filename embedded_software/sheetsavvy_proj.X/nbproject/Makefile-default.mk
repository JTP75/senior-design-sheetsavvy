#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=elf
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=hex
DEBUGGABLE_SUFFIX=elf
FINAL_IMAGE=${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}
endif

ifeq ($(COMPARE_BUILD), true)
COMPARISON_BUILD=-mafrlcsj
else
COMPARISON_BUILD=
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=time_detection.c user.c register_utils.c fft_utils.c peripheral_utils.c main.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/time_detection.o ${OBJECTDIR}/user.o ${OBJECTDIR}/register_utils.o ${OBJECTDIR}/fft_utils.o ${OBJECTDIR}/peripheral_utils.o ${OBJECTDIR}/main.o
POSSIBLE_DEPFILES=${OBJECTDIR}/time_detection.o.d ${OBJECTDIR}/user.o.d ${OBJECTDIR}/register_utils.o.d ${OBJECTDIR}/fft_utils.o.d ${OBJECTDIR}/peripheral_utils.o.d ${OBJECTDIR}/main.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/time_detection.o ${OBJECTDIR}/user.o ${OBJECTDIR}/register_utils.o ${OBJECTDIR}/fft_utils.o ${OBJECTDIR}/peripheral_utils.o ${OBJECTDIR}/main.o

# Source Files
SOURCEFILES=time_detection.c user.c register_utils.c fft_utils.c peripheral_utils.c main.c



CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk ${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=33EV256GM002
MP_LINKER_FILE_OPTION=,--script=p33EV256GM002.gld
# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/time_detection.o: time_detection.c  .generated_files/flags/default/826ccdcbcda1cbea79f50d97428264a26f2f4c8 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/time_detection.o.d 
	@${RM} ${OBJECTDIR}/time_detection.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  time_detection.c  -o ${OBJECTDIR}/time_detection.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/time_detection.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/user.o: user.c  .generated_files/flags/default/839558cf728e24d837244724ef157f290311ca1b .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/user.o.d 
	@${RM} ${OBJECTDIR}/user.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  user.c  -o ${OBJECTDIR}/user.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/user.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/register_utils.o: register_utils.c  .generated_files/flags/default/3ac7fd5b06055fbfe8fe4f49d687eea702b34adf .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/register_utils.o.d 
	@${RM} ${OBJECTDIR}/register_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  register_utils.c  -o ${OBJECTDIR}/register_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/register_utils.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/fft_utils.o: fft_utils.c  .generated_files/flags/default/6d6df6f69bd80825052369703dc7e4b73cd6d25e .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/fft_utils.o.d 
	@${RM} ${OBJECTDIR}/fft_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  fft_utils.c  -o ${OBJECTDIR}/fft_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/fft_utils.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/peripheral_utils.o: peripheral_utils.c  .generated_files/flags/default/d84c50749cc994953aa39a0043a12b4db551b7d5 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/peripheral_utils.o.d 
	@${RM} ${OBJECTDIR}/peripheral_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  peripheral_utils.c  -o ${OBJECTDIR}/peripheral_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/peripheral_utils.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/main.o: main.c  .generated_files/flags/default/b1a812c2075664cd1ee6bb1f55447f6925fc2725 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/main.o.d 
	@${RM} ${OBJECTDIR}/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  main.c  -o ${OBJECTDIR}/main.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/main.o.d"      -g -D__DEBUG     -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
else
${OBJECTDIR}/time_detection.o: time_detection.c  .generated_files/flags/default/644ec7aacb5e036f47ab48f372e2a989ed416eb5 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/time_detection.o.d 
	@${RM} ${OBJECTDIR}/time_detection.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  time_detection.c  -o ${OBJECTDIR}/time_detection.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/time_detection.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/user.o: user.c  .generated_files/flags/default/7da9729ed9db9f9f302eb15fe952325d27c25071 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/user.o.d 
	@${RM} ${OBJECTDIR}/user.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  user.c  -o ${OBJECTDIR}/user.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/user.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/register_utils.o: register_utils.c  .generated_files/flags/default/77d3e4db8ce3f4ef91b6d40cb312f1b28e998992 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/register_utils.o.d 
	@${RM} ${OBJECTDIR}/register_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  register_utils.c  -o ${OBJECTDIR}/register_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/register_utils.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/fft_utils.o: fft_utils.c  .generated_files/flags/default/8d7c062305823cc4674f5f78fbace93d4191724e .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/fft_utils.o.d 
	@${RM} ${OBJECTDIR}/fft_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  fft_utils.c  -o ${OBJECTDIR}/fft_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/fft_utils.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/peripheral_utils.o: peripheral_utils.c  .generated_files/flags/default/8bde20486668e81c7a233120b8fc414296fe52c6 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/peripheral_utils.o.d 
	@${RM} ${OBJECTDIR}/peripheral_utils.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  peripheral_utils.c  -o ${OBJECTDIR}/peripheral_utils.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/peripheral_utils.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
${OBJECTDIR}/main.o: main.c  .generated_files/flags/default/63f8794ffd02772e4f64f3142fa7a94e4e954397 .generated_files/flags/default/da39a3ee5e6b4b0d3255bfef95601890afd80709
	@${MKDIR} "${OBJECTDIR}" 
	@${RM} ${OBJECTDIR}/main.o.d 
	@${RM} ${OBJECTDIR}/main.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  main.c  -o ${OBJECTDIR}/main.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MP -MMD -MF "${OBJECTDIR}/main.o.d"        -g -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -mlarge-code -mlarge-data -mlarge-aggregate -O0 -msmart-io=1 -Wall -msfr-warn=off    -mdfp="${DFP_DIR}/xc16"
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemblePreproc
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: link
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  libdsp-elf.a  
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -o ${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}    libdsp-elf.a  -mcpu=$(MP_PROCESSOR_OPTION)        -D__DEBUG=__DEBUG   -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)   -mreserve=data@0x1000:0x101B -mreserve=data@0x101C:0x101D -mreserve=data@0x101E:0x101F -mreserve=data@0x1020:0x1021 -mreserve=data@0x1022:0x1023 -mreserve=data@0x1024:0x1027 -mreserve=data@0x1028:0x104F   -Wl,--no-local-stack,,--defsym=__MPLAB_BUILD=1,--defsym=__MPLAB_DEBUG=1,--defsym=__DEBUG=1,-D__DEBUG=__DEBUG,,$(MP_LINKER_FILE_OPTION),--heap=20,--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--report-mem,--memorysummary,${DISTDIR}/memoryfile.xml$(MP_EXTRA_LD_POST)  -mdfp="${DFP_DIR}/xc16" 
	
else
${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk  libdsp-elf.a 
	@${MKDIR} ${DISTDIR} 
	${MP_CC} $(MP_EXTRA_LD_PRE)  -o ${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}    libdsp-elf.a  -mcpu=$(MP_PROCESSOR_OPTION)        -omf=elf -DXPRJ_default=$(CND_CONF)    $(COMPARISON_BUILD)  -Wl,--no-local-stack,,--defsym=__MPLAB_BUILD=1,$(MP_LINKER_FILE_OPTION),--heap=20,--stack=16,--check-sections,--data-init,--pack-data,--handles,--isr,--no-gc-sections,--fill-upper=0,--stackguard=16,--no-force-link,--smart-io,-Map="${DISTDIR}/${PROJECTNAME}.${IMAGE_TYPE}.map",--report-mem,--memorysummary,${DISTDIR}/memoryfile.xml$(MP_EXTRA_LD_POST)  -mdfp="${DFP_DIR}/xc16" 
	${MP_CC_DIR}\\xc16-bin2hex ${DISTDIR}/first_draft_senior_design.X.${IMAGE_TYPE}.${DEBUGGABLE_SUFFIX} -a  -omf=elf   -mdfp="${DFP_DIR}/xc16" 
	
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r ${OBJECTDIR}
	${RM} -r ${DISTDIR}

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(wildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
