import cv2, time
import poseModule as pm
from scipy.spatial.distance import cosine
from fastdtw import fastdtw
import random

# 두 모델 또는 영상을 비교하는 함수입니다
def compare_positions(benchmark_video, user_video):
	# 벤치마크 캠은 대상이 될 모델 영상
	benchmark_cam = cv2.VideoCapture(benchmark_video)
	# 유저 캠은 플레이어의 모습이 보일 영상
	user_cam = cv2.VideoCapture(user_video)

	# FPS를 0으로 설정합니다
	fps_time = 0

	# 각 영상 별로 모션을 인식할 함수를 불러옵니다
	detector_1 = pm.poseDetector()
	detector_2 = pm.poseDetector()

	awesome_frame = 0
	great_frame = 0
	good_frame = 0
	ok_frame = 0
	bad_frame = 0

	# 영상의 시간 시간을 측정합니다
	start = int(time.time())

	# 게임의 랜덤 아이디를 생성합니다
	play_id = random.randrange(1, 100)

	# 정확도 계산이 끝난 시기를 저장할 변수
	capture_time = 0

	# 정확도 값을 저장할 변수
	global accuracyList
	accuracyList = []

	# 5초 간격으로 재설정되고 정확도 프레임 수와 계산될 프레임 수를 기록합니다
	frame_counter = 0

	# 영상의 총 길이를 초당 프레임 수로 기록합니다
	final_frame_counter = 0
	
	# 모션 인식 중 올바른 동작일 경우 해당 프레임 수를 저장합니다
	correct_frames = 0

	# 대상으로 쓰일 영상이나 유저의 캠이 정상적으로 켜진 경우
	while (benchmark_cam.isOpened() or user_cam.isOpened()):
		try:
			ret_val, image_1 = user_cam.read()
			
			# 해당 창을 특정 크기로 재설정합니다
			image_1 = cv2.resize(image_1, (720, 640))
			# 유저의 영상을 좌우 반전하여 거울 모드로 합니다
			image_1 = cv2.flip(image_1, 1)
			# 이미지의 모션을 인식합니다
			image_1 = detector_1.findPose(image_1)
			# 이미지의 위치를 인식합니다
			lmList_user = detector_1.findPosition(image_1)
			del lmList_user[1:11]
			
			ret_val_1, image_2 = benchmark_cam.read()

			# 해당 창을 특정 크기로 재설정합니다
			image_2 = cv2.resize(image_2, (720, 640))
			# 이미지의 모션을 인식합니다
			image_2 = detector_2.findPose(image_2)
			# 이미지의 위치를 인식합니다
			lmList_benchmark = detector_2.findPosition(image_2)
			del lmList_benchmark[1:11]

			# 모든 작업이 지나온 후 초당 프레임 수를 1개 올립니다
			frame_counter += 1
			final_frame_counter += 1

			if ret_val_1 or ret_val:
				# 유저의 영상과 모델의 영상을 코사인 유사도로 비교합니다
				error, _ = fastdtw(lmList_user, lmList_benchmark, dist = cosine)

				# 두 이미지를 비교하여 다른 값을 표시합니다
				cv2.putText(image_1, 'Error: {}%'.format(str(round(100*(float(error)),2))), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

				# 정화도가 90% 가 넘을 경우 정확한 동작으로 표시합니다
				if error < 0.15:
					cv2.putText(image_1, "CORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
					# 정확도를 측정 후 정확도 프레임 수를 1개 올립니다
					correct_frames += 1
				
				# 틀렸을 경우 틀린 동작으로 표시합니다
				else:
					cv2.putText(image_1, "INCORRECT STEPS", (40, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
				
				# 초당 프레임 수를 표시합니다
				cv2.putText(image_1, "FPS: %f" % (1.0 / (time.time() - fps_time)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

				# 유저의 캠 프레임 수를 측정합니다
				if frame_counter == 0:
					frame_counter = user_cam.get(cv2.CAP_PROP_FRAME_COUNT)

				# 올바른 동작 프레임 수를 총 플레이 타임 프레임 수를 나눠 백분율로 표기합니다
				cv2.putText(image_1, "Dance Steps Accurately Done: {}%".format(str(round(100*correct_frames/frame_counter, 2))), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)
				
				# 프레임 기록 시작 5초 후 계산될 시간을 기록합니다 
				end = int(time.time())

				if end - start >= 1:
					# 정확도가 90% 이상일 경우 Awesome 프레임 수를 올립니다
					if error < 0.01:
						awesome_frame += 1

					# 정확도가 80% 이상일 경우 Great 프레임 수를 올립니다
					elif error < 0.05 and error > 0.01:
						great_frame += 1

					# 정확도가 70% 이상일 경우 Good 프레임 수를 올립니다
					elif error < 0.3 and error > 0.05:
						good_frame += 1

					# 정확도가 60% 이상일 경우 OK 프레임 수를 올립니다
					elif error < 0.6 and error > 0.3:
						ok_frame += 1

					# 정확도가 60% 미만일 경우 Bad 프레임 수를 올립니다
					elif error > 0.6:
						bad_frame += 1
					
					print("\n")
					print("awesome", awesome_frame)
					print("great", great_frame)
					print("good", good_frame)
					print("ok", ok_frame)
					print("bad", bad_frame)

					start = int(time.time())

				if capture_time == 5:
					# 정확도 프레임 수를 총 프레임 수를 나누어 백분률로 표기
					print("Average", round(((awesome_frame + great_frame + good_frame + ok_frame)/frame_counter) * 100, 1))

				# 모델의 영상과 플레이어의 영상을 출력시킵니다
				cv2.imshow("Benchmark Video", image_2)
				cv2.imshow("User Video", image_1)

				cv2.moveWindow("Benchmark Video", 0, 0)
				cv2.moveWindow("User Video", 720, 0)

				# q 버튼을 누르면 모든 창을 종료합니다
				fps_time = time.time()
				if cv2.waitKey(1) & 0xFF == ord('q'):
					break

				# 모델의 영상이 끝난 경우 종료합니다
				if final_frame_counter == benchmark_cam.get(cv2.CAP_PROP_FRAME_COUNT):
					# 모델의 영상이 끝난 시간이 5초 단위로 기록된 가장 최근 기록과 중복될 경우 스킵합니다
					if capture_time == accuracyList[-1][-1]:
						break

					else:
						# 영상이 끝난 시점 기준의 캡쳐 시간을 측정합니다
						capture_time += (end - start)
						# 정확도 리스트에 플레이 아이디, 캡쳐 시간, 정확도를 추가하여 넣습니다
						accuracyList.append((play_id, capture_time, int(round(100*correct_frames/frame_counter, 2))))
						break
			else:
				break
		except:
			print("카메라에 인식할 대상이 없습니다")
			break

	# 영상 종료 후 모든 창을 종료해줍니다
	benchmark_cam.release()
	user_cam.release()
	cv2.destroyAllWindows()