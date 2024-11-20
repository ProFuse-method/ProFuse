# ProFuse
## [A Test Program Prioritization Method Based on Multi-Dimensional Feature Fusion for Logic Synthesis Tools Testing](https://github.com/ProFuse-method/ProFuse)
**The logic synthesis tools we tested include:**
1. **Commercial Logic Synthesis Tool Vivado (latest version 2023.2 and 2024.1)**
2. **Open Source Logic Synthesis Tool Yosys (latest version 0.30 + 48)**
***

**Env dependencies:**
1. **Vivado 2023.2 and 2024.1**
2. **Yosys 0.30 + 48**
3. **Icarus Verilog 13.0**
4. **Verismith 1.0.0.2**
5. **python 3.8**
6. **GHC 8.6.5**
7. **Cabal 3.6.0**
8. **Stack 2.9.3**
9. **HLS 2.0.0.1**
***

### Our Works
Logic synthesis tools translate hardware description languages (HDL) designs into hardware implementations.
To ensure the quality of these tools, tool developers spend tremendous time to execute test programs (i.e.,
HDL designs) for tool testing. However, only a small number of test programs can trigger faults. Although
test program prioritization has been proposed to accelerate this process by prior executing test programs with
high fault-triggering capability, existing prioritization methods are ineffective in accelerating logic synthesis
tool testing, due to the circuit-specific features of HDLs (e.g., timing logic). To this end, we propose ProFuse, a
multi-dimensional feature fusion method for logic synthesis tool test program prioritization. ProFuse leverages
Abstract Syntax Trees and Data Flow Graphs to extract novel syntactic and structure features from HDL
designs. These features are processed by a joint model of Multilayer Perceptron and Graph Convolutional
Network to rank fault-triggering test programs accurately. ProFuse achieves an Average Percentage of Fault
Detection (APFD) score of 0.9285, outperforming baselines by 11.38% to 82.49%. ProFuse can efficiently rank
randomly generated test programs to discover 15 new faults in logic synthesis tools (i.e., Yosys and Vivado),
while random testing uncovered only one fault within the same timeframe (i.e., two months).
***

### Main File
Our methodology is located in the 'main' directory:

1.The "main" folder:

This folder contains the implementation of our proposed method ProFuse, which includes:

ProFuse_main.py: The main function and core logic of ProFuse, which is responsible for feature fusion and fault prediction. It integrates both syntactic and structural features for effective logic synthesis tool analysis.

2.The "Program_Collection" folder:

This folder contains the dataset we collected for training and testing purposes. It includes various Verilog design files and test cases used in the evaluation of ProFuse.

3.The "Objective_Evaluation_Metrics" folder:

This folder contains the code for calculating the evaluation metrics used in the study. It includes metrics like APFD (Average Percentage of Faults Detected) to measure the effectiveness of the test program prioritization.

APFD.py: Calculates the APFD metric for evaluating the prioritization performance.

4.The "Feature_Preprocessing_code" folder:

This folder contains the code used for preprocessing features. It includes scripts for extracting syntactic and structural features from the Verilog design files.

get_syntactic_feature.py: Extracts syntactic features from the design files.
get_structure_feature.py: Extracts structural features based on the data flow and circuit connections.

5.The "baseline" folder:

This folder contains the implementations of the baseline algorithms used for comparison in our study. It includes:

baseline_LET.py: Implementation of the LET baseline algorithm.
baseline_MO-SDC.py: Implementation of the MO-SDC baseline algorithm.
baseline_RA.py: Implementation of the RA baseline algorithm.
baseline_TF-PS.py: Implementation of the TF-PS baseline algorithm.

6.The "Faults" folder:

Includes the faults discovered in the Vivado and Yosys logic synthesis tools. Each error file comes with a fault_description.pdf detailing the conditions that trigger the fault and an explanation of the error.
***

### Here are the details of these bugs
These errors in the error file can be reproduced using Vivado 2024.1 and Yosys 0.30+48.

You can find all fault files in path `method/bugs`.

Fault1：vivado	7mgyBdSAI	 A critical error during Vivado synthesis is surfacing in the DFPin::range() function.

Fault2：vivado	7oSDeISAW  An essential issue arises in Vivado synthesis, within the ConstProp::propagate() function.

Fault3：vivado	7qdVNFSA2	 In the course of Vivado synthesis, a critical error manifests within the NDes::optimize () function.

Fault4：vivado	7iVN3hSAG	 Vivado Synthesis Crashes Due to Exception in librdi_common.so.

Fault5：vivado	8S1pCRSAZ	 Vivado synthesis is running into an issue because the DFGraph::traverseTopDown() function is causing a crash.

Fault6：vivado	8TFwQ8SAL	 The HARTNDb::reSynthReInfer() function is crashing and causing a problem with Vivado synthesis.

Fault7：vivado	8TP2WdSAL	 Vivado synthesis is experiencing difficulties due to a crash in the ComMsgMgr::sendMessage() function.

Fault8：vivado	8VHDxiSAH	 Vivado synthesis failed by the HRTInvoker::inProcessLaunch() function.

Fault9：vivado	8gIPllSAG	 The LOptAbc::doOpt() function is causing an error that disrupts Vivado synthesis.

Fault10：vivado	8g0ri2SAA	 Vivado synthesis is failing because the NDes::optimizeLogic() function is crashing.

Fault11：vivado	8g0tKYSAY	 Vivado Synthesis Hang Issue with Specific Design File.

Fault12：vivado	8g0tqRSAQ	 Vivado Tool Synthesis Hanging Problem on Ubuntu.

Fault13：vivado	8UddyJSAR	 Vivado Hang During Synthesis with Specific Constraints.

Fault14：yosys	   4427	   Yosys Verilog Parsing Error: Unable to Synthesize After Reading File.

Fault15：yosys	   4445	   Performance Issue: Synthesis Takes Too Long to Complete.
***
**We've had so much help from Vivado and Yosys staff in finding and confirming bugs. I would like to express my gratitude here.**
