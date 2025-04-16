1. to create a branch other than main:
```
git branch
```

2. To switch through the branches:
```
git checkout branch name 
```

3. To merge into the main or any other branches:
a. check which branch you are in
b. if in main: 
```
git merge branch name
```
: the branch will be merged into main 

4. to delete a branch:
```
git branch -d branch name 
```

 Sensor Component Failure Prediction

Problem statement: 
1. The system in focus is the Air Pressure system (APS) which generates pressurized air that are utilized in various functions in a truck, such as braking and gear changes. The datasets positive class corresponds to component failures for a specific component of the APS system. The negative class corresponds to trucks with failures for components not related to the APS system.

2. The problem is to reduce the cost due to unnecessary repairs. So it is required to minimize the false predictions.

Challenges and other objectives: 
1. Need to Handle many Null values in almost all columns
2. No low-latency requirement.
3. Interpretability is not important.
4. Misclassification leads the unecessary repair costs.
