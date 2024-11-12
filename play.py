import time
from snake_env import SnakeEnv
CELL_SIZE = 10
def main():
    # Initialize the Snake environment
    env = SnakeEnv(grid_rows=CELL_SIZE, grid_cols=CELL_SIZE, render_mode='gui')
    
    # Reset the environment to start a new game
    obs, _ = env.reset()
    done = False
    
    # Play the game until it's done
    while not done:
        # Sample a random action
        action = env.action_space.sample()
        
        # Perform the action and receive the new observation, reward, and status
        obs, reward, done, _, _ = env.step(action)
        
        # Render the GUI to display the current state of the game
        env.render(mode='gui')
        
        # Slow down the gameplay for better visualization
        time.sleep(0.1)
    
    # Close the environment when done
    env.close()

if __name__ == "__main__":
    main()
