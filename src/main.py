from agent.agent import TaskPilotAgent


def main():
    agent=TaskPilotAgent()

    task="Process invoice INV-1042"

    result=agent.understand(task)

    print("TASK:",result["goal"])
    print("STATUS:",result["status"])

    plan=agent.create_plan()

    print("\nPLAN:")
    for i,step in enumerate(plan,1):
        print(f"{i}. {step}")

    execution=agent.execute()

    print("\nEXECUTION STATUS:",execution["status"])
    print("AGENT STATE:",agent.state.value)

    print("\nSTATE HISTORY:")
    for event in agent.state_history:
        print(f"{event['from']} -> {event['to']}")

    if execution["status"]=="completed":
        print("\nINVOICE FOUND:")
        print(execution["invoice"])

        print("\nFINANCE SYSTEM:",execution["finance_message"])
        print("VERIFIED:",execution["verified"])

        print("\nCOMPLETED STEPS:")
        for step in execution["completed_steps"]:
            print("-",step)

        print("\nTASKPILOT: TASK COMPLETED SUCCESSFULLY")
    else:
        print("\nERROR:",execution["error"])


if __name__=="__main__":
    main()