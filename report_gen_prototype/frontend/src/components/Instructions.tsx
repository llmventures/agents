import { useState } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; // Ensure Bootstrap is imported
import "bootstrap/dist/js/bootstrap.bundle.min"; // Import Bootstrap JS for modal functionality


interface InstructionsProps {
    startingShow: boolean; 
}

const Instructions: React.FC<InstructionsProps> = ({ startingShow }) => {
    const [show, setShow] = useState(startingShow);
  
    return (
      <>
        <button
          type="button"
          className="btn btn-primary"
          onClick={() => setShow(true)}
        >
          Instructions
        </button>
  
        {show && (
          <div className="modal fade show d-block" tabIndex={-1} role="dialog">
            <div className="modal-dialog" role="document">
              <div className="modal-content">
                <div className="modal-header">
                  <h5 className="modal-title">Instructions</h5>
                  <button
                    type="button"
                    className="btn-close"
                    onClick={() => setShow(false)}
                  ></button>
                </div>
                <div className="modal-body">
                <h2>Welcome to Agent based Report Generation</h2>
                <p>
                    This site provides an interface for generating reports through combining AI agents and Retrieval Augmented Generation.
                </p>

                <h3>Step 1: Getting Started</h3>
                <p>
                    Begin by navigating to "Leads" in the navbar above, and creating a lead. A lead is an agent that will remember the conversations and reports it generates, thus allowing it to use information learned from previous reports it has generated. The name and description fields are arbitrary and only serve to make it more clear for you the user.
                </p>

                <h3>Step 2: Building a team of potential agents</h3>
                <p>
                    Before generating a report, each lead chooses a team of agents. In the agents tab, you can create new agents that can be used in report generation. Role defines a role the agent takes within the report generation conversation, ie biologist, financial analyst, etc. For this application, the more industry specific you can make the role, the better.
                    Expertise expands on the role, giving more background information on the agent's domain of knowledge. For example, a biologist agent might have an expertise in genomic data anlysis. Be as specific as you can: think of role and expertise as a job description.
                    To give agents actual knowledge, upload papers in either pdf or text form when creating agents. Papers will be embedded, and drawn upon in an conversations where the agent speaks. 
                </p>

                <h3>Step 3: Creating a report</h3>
                <p>
                    Once you've created a lead and agents, it's time to generate a report. Name and description are arbitrary fields for the user. Task is the specific task you want to be addressed in the rpeort.
                    The report is generated through a conversation between agents: after the lead has assembled a team and assigned tasks and goals, it facilitates a conversation meant to address the task.

                    The report will address the expectations, for example, if you want the report to specifically discuss a certain feature,
                    Report guidelines describe features like how many words you want, the report formatting ,etc.

                    Users can also pass in context papers that can be the focus of the conversation. 

                    Potential agents is the list of agents the lead will choose from. This does not mean every agent will be a member of the conversation.

                    The cycle specifies the amount of times a full iteration of the conversation will run: ie, where each agent responds once.

                    Engine and model describe the AI engine used to generate responses.

                    Temperatures is a setting for the engine: higher temperatures lead to more creative answers.
                </p>

               

                </div>
                <div className="modal-footer">
                  <button
                    type="button"
                    className="btn btn-secondary"
                    onClick={() => setShow(false)}
                  >
                    Close
                  </button>
                  
                </div>
              </div>
            </div>
          </div>
        )}
  
        {show && <div className="modal-backdrop fade show"></div>}
      </>
    );
  };
  
  export default Instructions;