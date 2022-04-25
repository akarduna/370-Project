import TimelineItem from "@mui/lab/TimelineItem";
import TimelineSeparator from "@mui/lab/TimelineSeparator";
import TimelineConnector from "@mui/lab/TimelineConnector";
import TimelineContent from "@mui/lab/TimelineContent";
import TimelineDot from "@mui/lab/TimelineDot";
import TimelineOppositeContent from "@mui/lab/TimelineOppositeContent";
import { Avatar, Typography } from "@mui/material";
import DragonIcon from "../images/dragonIcon.png";

export default function TimelineDragon({ heartrate, type, time }) {
	return (
		<TimelineItem>
			<TimelineOppositeContent
				sx={{ m: "auto 0" }}
				align="right"
				variant="body2"
				color="text.secondary"
			>
				<Typography variant="body1">{heartrate} bpm</Typography>
				<Typography variant="body2">{time}</Typography>
			</TimelineOppositeContent>
			<TimelineSeparator>
				<TimelineConnector />
				<TimelineDot>
					<Avatar alt="Dragon" src={DragonIcon} />
				</TimelineDot>
				<TimelineConnector />
			</TimelineSeparator>
			<TimelineContent sx={{ py: "30px", px: 4 }}>
				<Typography variant="h6" component="span">
					Dragon
				</Typography>
				<Typography>{type}</Typography>
			</TimelineContent>
		</TimelineItem>
	);
}
