| Requirement Category     | Task Description                                                                                                       | Checkbox |
|--------------------------|------------------------------------------------------------------------------------------------------------------------|----------|
| General Requirements     | Code follows PEP 8 style guide                                                                                        | [X]      |
|                          | Code is documented with comments                                                                                       | [X]      |
|                          | Unit tests are created                                                                                                 | [X]      |
| MQTT Configuration       | **CarPark Class:**                                                                                                     |          |
|                          | Subscribes to MQTT topics                                                                                              | [X]      |
|                          | Publishes MQTT messages                                                                                                | [X]      |
|                          | Can parse messages from sensor                                                                          | [X]      |
|                          | Sends MQTT message that includes available bays, temperature                                                                         | [X]      |
|                          | **Sensor Class:**                                                                                                      |          |
|                          | Publishes MQTT messages                                                                                                | [X]      |
|                          | Sends MQTT messages that include temperature, time, and entry/exit                                                                                        | [X]      |
|                          | **Display Class:**                                                                                                     |          |
|                          | Subscribes to MQTT topics                                                                                              | [X]      |
|                          | Parses MQTT messages from car park                                                                                        | [X]      |
| Configuration File       | **CarPark Class:**                                                                                                     |          |
| Management               | Reads initial configuration from a file                                                                                | [X]      |
|                          | Writes available bays to a configuration class                                                                         | [X]      |
|                          | **Sensor Class:**                                                                                                      |          |
|                          | Reads initial configuration from a file                                                                                | [X]      |
|                          | **Display Class:**                                                                                                     |          |
|                          | Reads initial configuration from a file                                                                                | [X]      |
| Testing Requirements     | At least one test case for CarPark Class                                                                               | [ ]      |
|                          | At least one test case for Sensor or Display Class                                                                     | [ ]      |
| Additional Requirements  | Invent your own protocol for transmitting information; JSON is recommended                                             | [ ]      |
| Git Requirements         | Forked the original project repository                                                                                 | [X]      |
|                          | At least 3 local commits and 3 remote commits with reasonable messages                                                  | [X]      |
|                          | Worked in a feature branch and merged the feature branch                                                               | [X]      |
|                          | Both origin and local copy are synchronized at time of submission                                                      | [X]      |
| Submission Guidelines    | Code files organized in coherent folder structure                                                                      | [X]      |
|                          | Unit tests are submitted alongside the main code                                                                       | [ ]      |
|                          | Configuration files used for testing are included in the submission                                                    | [ ]      |
|                          | Submitted a zip file containing your code (excluding `venv/`, but including `.git/`)                                   | [X]      |
|                          | Ensure your lecturer has access to your GitHub repository                                                              | [X]      |
|                          | Completed the project journal                                                                                          | [ ]      |

Please use this updated table as a comprehensive guide for the project requirements. Ensure each task is completed and checked off before submitting your project for assessment.
Note there is a high-level (less detailed) checklist in the project journal, which is also used for grading. 
While there are a lot of items here, most items are small and can be addressed with 1-3 lines of code.
