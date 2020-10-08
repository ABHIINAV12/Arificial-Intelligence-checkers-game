from copy import deepcopy
import pygame

RED=(255,0,0)
WHITE=(255,255,255)

# positionrefers to where we are
# depth -> what depth we are at
# max_player-> are we min plyaer ?
# we only evaluate the position when we reach the end of the tree
# game is passed incase we need anything for visualization purposes
def minimax(position,depth,alpha,beta,max_player,game):
	if depth==0 or position.winner()!=None:
		return position.evaluate(),position
	if max_player:
		maxEval = float('-inf')
		best_move = None
		for move in get_all_moves(position,WHITE,game):
			evaluation = minimax(move,depth-1,alpha,beta,False,game)[0]
			maxEval=max(maxEval,evaluation)
			alpha=max(alpha,evaluation)
			if maxEval==evaluation:
				best_move=move
			if beta<=alpha:
				break
		return maxEval,best_move
	else:
		minEval = float('inf')
		best_move = None
		for move in get_all_moves(position,RED,game):
			evaluation = minimax(move,depth-1,alpha,beta,True,game)[0]
			minEval=min(minEval,evaluation)
			beta=min(beta,evaluation)
			if minEval==evaluation:
				best_move=move
			if beta<=alpha:
				break
		return minEval,best_move 

def stimulate_move(piece,move,board,game,skip):
	board.move(piece,move[0],move[1])
	if skip:
		board.remove(skip)
	return board

def get_all_moves(board,color,game):
	# moves store that if we move a particular piece then what will new board look like	
	moves=[]
	for piece in board.get_all_pieces(color):
		valid_moves=board.get_valid_moves(piece)
		# now items is a key nvalue pair (row,col): [pieces] describing how many pieces that we have to jump to reach row,col
		for move,skip in valid_moves.items():
			# move is a row,col tupple and skip is the list of pieces that we skip over
			temp_board=deepcopy(board)
			temp_piece=temp_board.get_piece(piece.row,piece.col)
			# take the piece and move it, skip if any and return the new board
			new_board=stimulate_move(temp_piece,move,temp_board,game,skip) 
			moves.append(new_board)
	return moves



